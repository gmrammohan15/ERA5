"""Session 9: observable causal-LM loss harness.

This file is executed by notebook.ipynb.  It is deliberately ordinary PyTorch
so every shape, shift, mask, loss, and memory measurement is inspectable.
"""

import gc
import math
import multiprocessing as mp
import random
import resource
import sys
import time
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


SEED = 9
random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
DTYPE = torch.float32


def section(title):
    print()
    print('=' * 78)
    print(title)
    print('=' * 78)


def show_shape(name, tensor, meaning):
    print(f'{name}: shape={tuple(tensor.shape)} | {meaning}')


def visible(token):
    return repr(token)


@dataclass
class CharTokenizer:
    chars: list
    pad: str = '<pad>'
    eos: str = '<eos>'

    def __post_init__(self):
        self.itos = [self.pad, self.eos] + self.chars
        self.stoi = {token: i for i, token in enumerate(self.itos)}
        self.pad_id = self.stoi[self.pad]
        self.eos_id = self.stoi[self.eos]

    @property
    def vocab_size(self):
        return len(self.itos)

    def encode(self, text, add_eos=True):
        ids = [self.stoi[ch] for ch in text]
        if add_eos:
            ids.append(self.eos_id)
        return ids

    def decode_id(self, token_id):
        return self.itos[int(token_id)]


DOC_A = (
    'To be, or not to be, that is the question: Whether tis nobler in the mind '
    'to suffer the slings and arrows of outrageous fortune.'
)
DOC_B = (
    "All the world's a stage, and all the men and women merely players; they "
    'have their exits and their entrances.'
)
DOC_C = (
    'The quality of mercy is not strained. It droppeth as the gentle rain from '
    'heaven upon the place beneath.'
)
CORPUS_DOCS = [DOC_A, DOC_B, DOC_C]
CORPUS = '\n'.join(CORPUS_DOCS)
TOKENIZER = CharTokenizer(sorted(set(CORPUS)))
VOCAB_SIZE = TOKENIZER.vocab_size

BLOCK_SIZE = 64
D_MODEL = 96
N_HEAD = 4
N_LAYER = 2
BATCH_SIZE = 8


class TinyCausalLM(nn.Module):
    def __init__(self, vocab_size, max_len, d_model=D_MODEL, n_head=N_HEAD, n_layer=N_LAYER):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_embedding = nn.Embedding(max_len, d_model)
        layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=n_head,
            dim_feedforward=4 * d_model,
            dropout=0.0,
            activation='gelu',
            batch_first=True,
            norm_first=True,
        )
        self.blocks = nn.TransformerEncoder(layer, num_layers=n_layer)
        self.final_norm = nn.LayerNorm(d_model)
        self.max_len = max_len

    def forward(self, tokens):
        _, length = tokens.shape
        if length > self.max_len:
            raise ValueError(f'sequence length {length} exceeds {self.max_len}')
        positions = torch.arange(length, device=tokens.device)
        x = self.token_embedding(tokens) + self.position_embedding(positions)[None, :, :]
        causal_mask = torch.triu(
            torch.ones(length, length, device=tokens.device, dtype=torch.bool), diagonal=1
        )
        return self.final_norm(self.blocks(x, mask=causal_mask))


class OutputHead(nn.Module):
    def __init__(self, d_model, vocab_size):
        super().__init__()
        self.proj = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, hidden):
        return self.proj(hidden)


def masked_cross_entropy(logits, targets, mask=None):
    flat_logits = logits.reshape(-1, logits.shape[-1])
    flat_targets = targets.reshape(-1)
    if mask is None:
        return F.cross_entropy(flat_logits, flat_targets)
    flat_mask = mask.reshape(-1).bool()
    if int(flat_mask.sum()) == 0:
        raise ValueError('loss mask contains no contributing tokens')
    return F.cross_entropy(flat_logits[flat_mask], flat_targets[flat_mask])


def padded_tokens(texts):
    rows = [TOKENIZER.encode(text, add_eos=True) for text in texts]
    width = max(len(row) for row in rows)
    tokens = torch.full((len(rows), width), TOKENIZER.pad_id, dtype=torch.long)
    for row_index, row in enumerate(rows):
        tokens[row_index, :len(row)] = torch.tensor(row)
    return tokens


def token_strings(row):
    return [TOKENIZER.decode_id(token_id) for token_id in row.tolist()]


def unique_parameter_count(module):
    seen = set()
    total = 0
    for parameter in module.parameters():
        if id(parameter) not in seen:
            total += parameter.numel()
            seen.add(id(parameter))
    return total


def print_shift_table(tokens, limit=24):
    section('1. Shift verification: strings, not token ids')
    inputs = tokens[:, :-1]
    targets = tokens[:, 1:]
    show_shape('tokens', tokens, 'B=batch rows, T=token positions')
    show_shape('inputs', inputs, 'B=batch rows, T-1 source positions')
    show_shape('targets', targets, 'B=batch rows, T-1 next-token labels')
    print('pos | input string | target string | expected target string')
    print('----|--------------|---------------|----------------------')
    strings = token_strings(tokens[0])
    for position in range(min(limit, inputs.shape[1])):
        print(
            f'{position:>3} | {visible(strings[position]):>12} | '
            f'{visible(strings[position + 1]):>13} | {visible(strings[position + 1])}'
        )
    assert torch.equal(inputs[0, 1:], targets[0, :-1])
    print('CHECK: every displayed target is the string immediately to the right of its input.')
    return inputs, targets


def copy_shift_diagnostic(tokens):
    section('2. Reading-based Part 3 demonstration: the unshifted bug')
    source = tokens[:, :-1]
    target_next = tokens[:, 1:]
    target_same = tokens[:, :-1]
    logits = torch.zeros(1, source.shape[1], VOCAB_SIZE)
    for position, token_id in enumerate(source[0].tolist()):
        logits[0, position, token_id] = 8.0
    correct = F.cross_entropy(logits.reshape(-1, VOCAB_SIZE), target_next.reshape(-1))
    wrong = F.cross_entropy(logits.reshape(-1, VOCAB_SIZE), target_same.reshape(-1))
    print(f'copy-biased diagnostic loss with correct t+1 targets: {correct.item():.6f}')
    print(f'copy-biased diagnostic loss with incorrect same-position targets: {wrong.item():.6f}')
    print('The low same-position number is not next-token skill; it rewards copying the input.')
    return correct.item(), wrong.item()


def padding_demo(model, head):
    section('3. Padding mask: count changes and padded targets are not learned')
    tokens = padded_tokens([DOC_A[:58], DOC_B[:27]])
    inputs, targets = tokens[:, :-1].to(DEVICE), tokens[:, 1:].to(DEVICE)
    with torch.no_grad():
        hidden = model(tokens.to(DEVICE))
        logits = head(hidden[:, :-1])
    mask = targets.ne(TOKENIZER.pad_id)
    show_shape('padded tokens', tokens, 'B=batch rows, T=max padded sequence length')
    show_shape('padding loss mask', mask, 'B=batch rows, T-1; True means contributes to loss')
    show_shape('hidden', hidden, 'B=batch rows, T, D=hidden width')
    show_shape('logits', logits, 'B=batch rows, T-1, V=vocabulary size')
    print(f'unmasked contributing positions: {targets.numel()}')
    print(f'masked contributing positions:   {int(mask.sum())}')
    diagnostic_logits = logits.detach().clone()
    pad_positions = targets.eq(TOKENIZER.pad_id)
    pad_column = diagnostic_logits[..., TOKENIZER.pad_id]
    diagnostic_logits[..., TOKENIZER.pad_id] = torch.where(
        pad_positions, torch.full_like(pad_column, 8.0), pad_column
    )
    before = masked_cross_entropy(diagnostic_logits, targets)
    after = masked_cross_entropy(diagnostic_logits, targets, mask)
    print(f'loss before padding mask: {before.item():.6f}')
    print(f'loss after padding mask:  {after.item():.6f}')
    print('The diagnostic makes PAD easy to predict; counting it would reward a shortcut.')
    assert int(mask.sum()) < targets.numel()
    return {
        'positions_before': int(targets.numel()),
        'positions_after': int(mask.sum()),
        'loss_before': before.item(),
        'loss_after': after.item(),
    }


def pack_two_documents():
    ids_a = TOKENIZER.encode(DOC_A, add_eos=True)
    ids_b = TOKENIZER.encode(DOC_B, add_eos=True)
    ids = ids_a + ids_b
    document_ids = [0] * len(ids_a) + [1] * len(ids_b)
    tokens = torch.tensor(ids, dtype=torch.long).unsqueeze(0)
    return tokens, torch.tensor(document_ids, dtype=torch.long).unsqueeze(0)


def boundary_demo(model, head):
    section('4. Packed documents: mask the cross-document boundary')
    tokens, document_ids = pack_two_documents()
    source = tokens[:, :-1].to(DEVICE)
    targets = tokens[:, 1:].to(DEVICE)
    same_document = document_ids[:, :-1].eq(document_ids[:, 1:]).to(DEVICE)
    pack_model = model
    pack_head = head
    if tokens.shape[1] > model.max_len:
        pack_model = TinyCausalLM(VOCAB_SIZE, tokens.shape[1]).to(DEVICE)
        pack_head = OutputHead(D_MODEL, VOCAB_SIZE).to(DEVICE)
        with torch.no_grad():
            pack_head.proj.weight.zero_()
    with torch.no_grad():
        hidden = pack_model(tokens.to(DEVICE))
        logits = pack_head(hidden[:, :-1])
    show_shape('packed tokens', tokens, 'B=1 packed document row, T=doc A + EOS + doc B + EOS')
    show_shape('document ids', document_ids, 'B=1, T; integer provenance label for each token')
    show_shape('boundary mask', same_document, 'B=1, T-1; False excludes cross-document target')
    boundary_positions = (~same_document[0]).nonzero(as_tuple=False).flatten().tolist()
    print(f'unmasked target positions: {targets.numel()}')
    print(f'within-document target positions: {int(same_document.sum())}')
    print(f'cross-document boundary positions masked: {len(boundary_positions)}')
    for position in boundary_positions:
        input_string = TOKENIZER.decode_id(int(source[0, position]))
        target_string = TOKENIZER.decode_id(int(targets[0, position]))
        print(f'boundary at position {position}: input {visible(input_string)} -> target {visible(target_string)}')
    diagnostic_logits = logits.detach().clone()
    for position in boundary_positions:
        target_id = int(targets[0, position])
        diagnostic_logits[0, position, target_id] = 8.0
    before = masked_cross_entropy(diagnostic_logits, targets)
    after = masked_cross_entropy(diagnostic_logits, targets, same_document)
    print(f'loss before boundary mask: {before.item():.6f}')
    print(f'loss after boundary mask:  {after.item():.6f}')
    print('Only the loss target is masked here, matching the lecture\'s master-target explanation.')
    assert int(same_document.sum()) == targets.numel() - len(boundary_positions)
    return {
        'loss_before': before.item(),
        'loss_after': after.item(),
        'boundary_count': len(boundary_positions),
    }


def shape_and_perplexity_demo():
    section('5. Complete harness and untrained perplexity sanity check')
    model = TinyCausalLM(VOCAB_SIZE, BLOCK_SIZE).to(DEVICE)
    head = OutputHead(D_MODEL, VOCAB_SIZE).to(DEVICE)
    with torch.no_grad():
        head.proj.weight.zero_()
    tokens = padded_tokens([DOC_A[:BLOCK_SIZE - 2], DOC_B[:BLOCK_SIZE - 2]])
    tokens = tokens.to(DEVICE)
    inputs = tokens[:, :-1]
    targets = tokens[:, 1:]
    loss_mask = targets.ne(TOKENIZER.pad_id)
    hidden = model(inputs)
    logits = head(hidden)
    flat_logits = logits.reshape(-1, VOCAB_SIZE)
    flat_targets = targets.reshape(-1)
    flat_mask = loss_mask.reshape(-1)
    show_shape('input tokens', inputs, 'B=batch rows, T-1 source token positions')
    show_shape('target tokens', targets, 'B=batch rows, T-1 next-token labels')
    show_shape('hidden', hidden, 'B=batch rows, T-1, D=hidden dimension')
    show_shape('output-head weight', head.proj.weight, 'V=vocabulary rows, D=hidden columns')
    show_shape('logits', logits, 'B=batch rows, T-1, V=one score per vocabulary token')
    show_shape('flat logits', flat_logits, 'B*(T-1) flattened positions, V classes')
    show_shape('flat targets', flat_targets, 'B*(T-1) flattened labels')
    show_shape('flat mask', flat_mask, 'B*(T-1) flattened validity flags')
    loss = masked_cross_entropy(logits, targets, loss_mask)
    perplexity = loss.exp()
    expected = math.log(VOCAB_SIZE)
    print(f'vocab_size={VOCAB_SIZE}')
    print(f'untrained zero-head loss={loss.item():.6f}; expected ln(V)={expected:.6f}')
    print(f'untrained perplexity={perplexity.item():.6f}; expected V={VOCAB_SIZE}')
    assert abs(loss.item() - expected) < 1e-5
    return model, head, {'loss': loss.item(), 'perplexity': perplexity.item()}


def parameter_demo(model):
    section('6. Tied versus untied output-head parameter counts')
    tied = nn.Module()
    tied.embedding = nn.Embedding(VOCAB_SIZE, D_MODEL)
    untied = nn.Module()
    untied.embedding = nn.Embedding(VOCAB_SIZE, D_MODEL)
    untied.head = nn.Linear(D_MODEL, VOCAB_SIZE, bias=False)
    embedding_params = VOCAB_SIZE * D_MODEL
    model_params_including_embedding = unique_parameter_count(model)
    body_params_excluding_embedding = model_params_including_embedding - embedding_params
    tied_total = model_params_including_embedding
    untied_head_params = VOCAB_SIZE * D_MODEL
    untied_total = model_params_including_embedding + untied_head_params
    print(f'configuration: V={VOCAB_SIZE}, D={D_MODEL}, bias=False')
    print(f'Transformer body excluding input embedding: {body_params_excluding_embedding:,}')
    print(f'input embedding parameters: {embedding_params:,}')
    print(f'tied head additional parameters: 0 (uses embedding weight transpose)')
    print(f'tied unique model parameters: {tied_total:,}')
    print(f'untied head parameters: {untied_head_params:,}')
    print(f'untied unique model parameters: {untied_total:,}')
    print(f'untied minus tied: {untied_total - tied_total:,}')
    return {
        'tied_head_additional': 0,
        'untied_head': untied_head_params,
        'tied_total': tied_total,
        'untied_total': untied_total,
    }


def ordinary_ce(hidden, weight, targets):
    logits = F.linear(hidden, weight)
    return F.cross_entropy(logits, targets)


def chunked_ce(hidden, weight, targets, chunk_size):
    total = hidden.new_zeros(())
    for start in range(0, hidden.shape[0], chunk_size):
        logits = F.linear(hidden[start:start + chunk_size], weight)
        total = total + F.cross_entropy(logits, targets[start:start + chunk_size], reduction='sum')
        del logits
    return total / targets.numel()


def memory_case(kind, device, shape, vocab_size, chunk_size):
    rows, d_model = shape
    hidden = torch.randn(rows, d_model, device=device, dtype=DTYPE)
    weight = torch.randn(vocab_size, d_model, device=device, dtype=DTYPE)
    targets = torch.randint(vocab_size, (rows,), device=device)
    if device.type == 'cuda':
        torch.cuda.synchronize()
        baseline = torch.cuda.memory_allocated(device)
        torch.cuda.reset_peak_memory_stats(device)
    else:
        baseline = 0
    with torch.no_grad():
        if kind == 'ordinary':
            loss = ordinary_ce(hidden, weight, targets)
        else:
            loss = chunked_ce(hidden, weight, targets, chunk_size)
    if device.type == 'cuda':
        torch.cuda.synchronize()
        peak = torch.cuda.max_memory_allocated(device) - baseline
    else:
        peak = 0
    value = loss.item()
    del hidden, weight, targets, loss
    if device.type == 'cuda':
        torch.cuda.empty_cache()
    return value, peak


def _cpu_memory_worker(kind, connection, rows, d_model, vocab_size, chunk_size):
    hidden = torch.randn(rows, d_model, dtype=DTYPE)
    weight = torch.randn(vocab_size, d_model, dtype=DTYPE)
    targets = torch.randint(vocab_size, (rows,))
    gc.collect()
    baseline = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    with torch.no_grad():
        if kind == 'ordinary':
            loss = ordinary_ce(hidden, weight, targets)
        else:
            loss = chunked_ce(hidden, weight, targets, chunk_size)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    unit = 1 if sys.platform == 'darwin' else 1024
    connection.send({'loss': loss.item(), 'peak_bytes': max(0, peak - baseline) * unit})
    connection.close()


def cpu_memory_case(kind, rows, d_model, vocab_size, chunk_size):
    methods = mp.get_all_start_methods()
    if 'fork' not in methods:
        return memory_case(kind, torch.device('cpu'), (rows, d_model), vocab_size, chunk_size)
    context = mp.get_context('fork')
    parent, child = context.Pipe(False)
    process = context.Process(
        target=_cpu_memory_worker,
        args=(kind, child, rows, d_model, vocab_size, chunk_size),
    )
    process.start()
    result = parent.recv()
    process.join()
    return result['loss'], result['peak_bytes']


def memory_demo():
    section('7. Ordinary versus chunked cross-entropy memory')
    rows = 2 * 768
    memory_d = 128
    memory_v = 8192
    chunk_size = 128
    if DEVICE.type == 'cuda':
        ordinary_loss, ordinary_peak = memory_case(
            'ordinary', DEVICE, (rows, memory_d), memory_v, chunk_size
        )
        chunked_loss, chunked_peak = memory_case(
            'chunked', DEVICE, (rows, memory_d), memory_v, chunk_size
        )
        unit = 'CUDA max allocated bytes above baseline'
    else:
        ordinary_loss, ordinary_peak = cpu_memory_case(
            'ordinary', rows, memory_d, memory_v, chunk_size
        )
        chunked_loss, chunked_peak = cpu_memory_case(
            'chunked', rows, memory_d, memory_v, chunk_size
        )
        unit = 'child-process peak RSS above input baseline'
    ordinary_mb = ordinary_peak / (1024 ** 2)
    chunked_mb = chunked_peak / (1024 ** 2)
    ratio = ordinary_mb / chunked_mb if chunked_mb else float('nan')
    print(f'device={DEVICE}; rows={rows}; D={memory_d}; V={memory_v}; chunk={chunk_size}')
    print(f'measurement={unit}')
    print(f'ordinary loss={ordinary_loss:.6f}; peak memory={ordinary_mb:.3f} MiB')
    print(f'chunked loss={chunked_loss:.6f}; peak memory={chunked_mb:.3f} MiB')
    print(f'ordinary/chunked memory ratio={ratio:.3f}x')
    print(f'loss absolute difference={abs(ordinary_loss - chunked_loss):.9f}')
    assert abs(ordinary_loss - chunked_loss) < 1e-5
    return {
        'ordinary_mb': ordinary_mb,
        'chunked_mb': chunked_mb,
        'ratio': ratio,
        'loss_difference': abs(ordinary_loss - chunked_loss),
    }


def stream_batch(stream, batch_size, length, device):
    starts = torch.randint(0, len(stream) - length, (batch_size,))
    batch = torch.stack([stream[int(start):int(start) + length] for start in starts])
    return batch.to(device)


def mtp_training_demo():
    section('8. Part 2: one extra head predicts t+2')
    stream_ids = []
    for _ in range(80):
        for document in CORPUS_DOCS:
            stream_ids.extend(TOKENIZER.encode(document, add_eos=True))
    stream = torch.tensor(stream_ids, dtype=torch.long)
    model = TinyCausalLM(VOCAB_SIZE, BLOCK_SIZE).to(DEVICE)
    head_one = OutputHead(D_MODEL, VOCAB_SIZE).to(DEVICE)
    head_two = OutputHead(D_MODEL, VOCAB_SIZE).to(DEVICE)
    optimizer = torch.optim.AdamW(
        list(model.parameters()) + list(head_one.parameters()) + list(head_two.parameters()),
        lr=3e-3,
        weight_decay=0.0,
    )
    history = []
    steps = 180
    for step in range(steps + 1):
        batch = stream_batch(stream, BATCH_SIZE, BLOCK_SIZE + 2, DEVICE)
        context = batch[:, :-2]
        target_one = batch[:, 1:-1]
        target_two = batch[:, 2:]
        hidden = model(context)
        logits_one = head_one(hidden)
        logits_two = head_two(hidden)
        loss_one = masked_cross_entropy(logits_one, target_one)
        loss_two = masked_cross_entropy(logits_two, target_two)
        total = loss_one + loss_two
        if step == 0 or step == steps or step % 20 == 0:
            history.append((step, loss_one.item(), loss_two.item(), total.item()))
            print(
                f'step {step:>3}: head t+1={loss_one.item():.6f}; '
                f'head t+2={loss_two.item():.6f}; sum={total.item():.6f}'
            )
        if step < steps:
            optimizer.zero_grad(set_to_none=True)
            total.backward()
            optimizer.step()
    initial = history[0]
    final = history[-1]
    try:
        import matplotlib.pyplot as plt

        steps_seen = [row[0] for row in history]
        loss_one_seen = [row[1] for row in history]
        loss_two_seen = [row[2] for row in history]
        plt.figure(figsize=(7, 4))
        plt.plot(steps_seen, loss_one_seen, marker='o', label='head t+1')
        plt.plot(steps_seen, loss_two_seen, marker='o', label='head t+2')
        plt.xlabel('training step')
        plt.ylabel('cross-entropy loss')
        plt.title('Multi-head next-token training')
        plt.grid(alpha=0.25)
        plt.legend()
        plt.tight_layout()
        if 'IPython' in sys.modules:
            plt.show()
        else:
            plot_path = '/tmp/session9_mtp_curve.png'
            plt.savefig(plot_path, dpi=140)
            plt.close()
            print(f'curve saved to {plot_path}')
    except ImportError:
        print('matplotlib is unavailable; the printed checkpoints are the training curve.')
    print(
        'Observation: compare the two curves rather than assuming equality. '
        'The t+2 head has less local information and is normally higher/slower.'
    )
    return {
        'history': history,
        'head_t_plus_1_loss': final[1],
        'head_t_plus_2_loss': final[2],
        'sum_loss': final[3],
        'initial_t_plus_1': initial[1],
        'initial_t_plus_2': initial[2],
    }


def run():
    section('Session 9 loss harness')
    print(f'device={DEVICE}; torch={torch.__version__}; seed={SEED}')
    print(f'vocab_size={VOCAB_SIZE}; block_size={BLOCK_SIZE}; D={D_MODEL}; heads={N_HEAD}; layers={N_LAYER}')
    print('tokens are characters plus <pad> and <eos>; whitespace is shown with repr().')
    sample = padded_tokens([DOC_A[:BLOCK_SIZE - 2]])
    print_shift_table(sample)
    shift_correct, shift_wrong = copy_shift_diagnostic(sample)
    model, head, untrained = shape_and_perplexity_demo()
    padding = padding_demo(model, head)
    boundary = boundary_demo(model, head)
    parameters = parameter_demo(model)
    memory = memory_demo()
    mtp = mtp_training_demo()
    section('Machine-readable result summary')
    results = {
        'vocab_size': VOCAB_SIZE,
        'part3_correct_shift_loss': shift_correct,
        'part3_wrong_unshifted_loss': shift_wrong,
        'padding': padding,
        'boundary': boundary,
        'untrained': untrained,
        'parameters': parameters,
        'memory': memory,
        'mtp': {key: value for key, value in mtp.items() if key != 'history'},
    }
    for key, value in results.items():
        print(f'{key}: {value}')
    return results


if __name__ == '__main__':
    run()
