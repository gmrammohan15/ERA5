from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import torch
import torch.nn.functional as F
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence


EOS = 256
BOS = 257
BYTE_CLASSES = 257


class TokenByteCodec:
    """Reversible serialization of tokenizer-internal token strings."""

    def __init__(self, vocab: list[str], max_bytes: int = 128) -> None:
        self.vocab = vocab
        self.max_bytes = max_bytes
        self.sequences: list[tuple[int, ...]] = []
        self.known: dict[bytes, int] = {}
        for token_id, token in enumerate(vocab):
            raw = token.encode("utf-8")
            if len(raw) > max_bytes:
                raise ValueError(
                    f"vocabulary token {token_id} needs {len(raw)} bytes; max is {max_bytes}"
                )
            values = tuple(raw)
            self.sequences.append(values)
            self.known[raw] = token_id
        self.lengths = torch.tensor([len(seq) for seq in self.sequences], dtype=torch.long)

    def bytes_for_id(self, token_id: int) -> bytes:
        return bytes(self.sequences[token_id])

    def id_for_bytes(self, value: bytes) -> int | None:
        return self.known.get(value)

    def valid_utf8(self, value: bytes) -> bool:
        try:
            value.decode("utf-8", errors="strict")
            return True
        except UnicodeDecodeError:
            return False

    def roundtrip_ok(self) -> bool:
        return all(self.vocab[i].encode("utf-8") == self.bytes_for_id(i) for i in range(len(self.vocab)))

    def batch_sequences(self, token_ids: torch.Tensor) -> list[tuple[int, ...]]:
        ids = token_ids.detach().reshape(-1).cpu().tolist()
        return [self.sequences[int(idx)] for idx in ids]

    def byte_lengths(self, token_ids: torch.Tensor, device: torch.device | None = None) -> torch.Tensor:
        ids = token_ids.detach().reshape(-1).cpu()
        values = self.lengths[ids]
        return values.to(device or token_ids.device)

    def teacher_forcing_tensors(
        self, token_ids: torch.Tensor, device: torch.device
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        sequences = self.batch_sequences(token_ids)
        lengths = torch.tensor([len(seq) + 1 for seq in sequences], device=device, dtype=torch.long)
        max_steps = int(lengths.max().item())
        inputs = torch.full((len(sequences), max_steps), BOS, device=device, dtype=torch.long)
        targets = torch.full((len(sequences), max_steps), EOS, device=device, dtype=torch.long)
        for row, seq in enumerate(sequences):
            n = len(seq)
            if n:
                raw = torch.tensor(seq, device=device, dtype=torch.long)
                inputs[row, 1 : n + 1] = raw
                targets[row, :n] = raw
            targets[row, n] = EOS
        return inputs, targets, lengths


@dataclass
class HeadLoss:
    loss: torch.Tensor
    token_nll: torch.Tensor
    byte_lengths: torch.Tensor
    peak_logits_bytes: int


class VocabularyHead(nn.Module):
    name = "vocabulary"

    def __init__(self, d_model: int, vocab_size: int) -> None:
        super().__init__()
        self.projection = nn.Linear(d_model, vocab_size)

    def loss(
        self, hidden: torch.Tensor, token_ids: torch.Tensor, codec: TokenByteCodec
    ) -> HeadLoss:
        logits = self.projection(hidden)
        targets = token_ids.reshape(-1)
        token_nll = F.cross_entropy(logits, targets, reduction="none")
        return HeadLoss(
            loss=token_nll.mean(),
            token_nll=token_nll,
            byte_lengths=codec.byte_lengths(targets, logits.device),
            peak_logits_bytes=logits.numel() * logits.element_size(),
        )

    @torch.no_grad()
    def greedy_bytes(self, hidden: torch.Tensor, codec: TokenByteCodec) -> list[bytes]:
        ids = self.projection(hidden).argmax(dim=-1).cpu().tolist()
        return [codec.bytes_for_id(int(idx)) for idx in ids]

    @torch.no_grad()
    def topk_bytes(
        self, hidden: torch.Tensor, codec: TokenByteCodec, width: int
    ) -> list[list[bytes]]:
        ids = self.projection(hidden).topk(width, dim=-1).indices.cpu().tolist()
        return [[codec.bytes_for_id(int(idx)) for idx in row] for row in ids]


class ParallelByteHead(nn.Module):
    name = "parallel_byte"

    def __init__(self, d_model: int, hidden_dim: int = 128, max_bytes: int = 128) -> None:
        super().__init__()
        self.max_bytes = max_bytes
        self.state_projection = nn.Linear(d_model, hidden_dim)
        self.position = nn.Embedding(max_bytes + 1, hidden_dim)
        self.classifier = nn.Linear(hidden_dim, BYTE_CLASSES)

    def _flat_training_data(
        self, token_ids: torch.Tensor, codec: TokenByteCodec, device: torch.device
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        sequences = codec.batch_sequences(token_ids)
        lengths = torch.tensor([len(seq) + 1 for seq in sequences], device=device, dtype=torch.long)
        positions = torch.cat(
            [torch.arange(int(length), device=device) for length in lengths.cpu().tolist()]
        )
        targets = torch.cat(
            [torch.tensor((*seq, EOS), device=device, dtype=torch.long) for seq in sequences]
        )
        token_index = torch.repeat_interleave(
            torch.arange(len(sequences), device=device), lengths
        )
        return lengths, positions, targets, token_index

    def loss(
        self, hidden: torch.Tensor, token_ids: torch.Tensor, codec: TokenByteCodec
    ) -> HeadLoss:
        hidden = hidden.reshape(-1, hidden.shape[-1])
        targets_ids = token_ids.reshape(-1)
        lengths, positions, targets, token_index = self._flat_training_data(
            targets_ids, codec, hidden.device
        )
        base = self.state_projection(hidden)
        features = torch.tanh(base[token_index] + self.position(positions))
        logits = self.classifier(features)
        step_nll = F.cross_entropy(logits, targets, reduction="none")
        token_nll = torch.zeros(len(hidden), device=hidden.device)
        token_nll.scatter_add_(0, token_index, step_nll)
        return HeadLoss(
            loss=token_nll.mean(),
            token_nll=token_nll,
            byte_lengths=lengths - 1,
            peak_logits_bytes=logits.numel() * logits.element_size(),
        )

    @torch.no_grad()
    def greedy_bytes(self, hidden: torch.Tensor, codec: TokenByteCodec) -> list[bytes]:
        hidden = hidden.reshape(-1, hidden.shape[-1])
        positions = torch.arange(self.max_bytes + 1, device=hidden.device)
        base = self.state_projection(hidden)[:, None, :]
        features = torch.tanh(base + self.position(positions)[None, :, :])
        predicted = self.classifier(features).argmax(dim=-1).cpu().tolist()
        outputs: list[bytes] = []
        for row in predicted:
            values: list[int] = []
            for value in row:
                if value == EOS:
                    break
                values.append(int(value))
                if len(values) == self.max_bytes:
                    break
            outputs.append(bytes(values))
        return outputs

    @torch.no_grad()
    def topk_bytes(
        self, hidden: torch.Tensor, codec: TokenByteCodec, width: int
    ) -> list[list[bytes]]:
        # Independent positions do not define a meaningful sequence beam. Keep
        # the greedy sequence as the sole structured candidate.
        return [[value] for value in self.greedy_bytes(hidden, codec)]


class AutoregressiveByteHead(nn.Module):
    name = "autoregressive_byte"

    def __init__(
        self,
        d_model: int,
        byte_embedding_dim: int = 64,
        hidden_dim: int = 128,
        max_bytes: int = 128,
    ) -> None:
        super().__init__()
        self.max_bytes = max_bytes
        self.hidden_dim = hidden_dim
        self.byte_embedding = nn.Embedding(258, byte_embedding_dim)
        self.initial = nn.Linear(d_model, hidden_dim)
        self.gru = nn.GRU(byte_embedding_dim, hidden_dim, batch_first=True)
        self.classifier = nn.Linear(hidden_dim, BYTE_CLASSES)

    def loss(
        self, hidden: torch.Tensor, token_ids: torch.Tensor, codec: TokenByteCodec
    ) -> HeadLoss:
        hidden = hidden.reshape(-1, hidden.shape[-1])
        targets_ids = token_ids.reshape(-1)
        inputs, targets, lengths = codec.teacher_forcing_tensors(targets_ids, hidden.device)
        embedded = self.byte_embedding(inputs)
        packed_inputs = pack_padded_sequence(
            embedded, lengths.cpu(), batch_first=True, enforce_sorted=False
        )
        h0 = self.initial(hidden).unsqueeze(0)
        packed_outputs, _ = self.gru(packed_inputs, h0)
        logits = self.classifier(packed_outputs.data)

        packed_targets = pack_padded_sequence(
            targets, lengths.cpu(), batch_first=True, enforce_sorted=False
        ).data
        token_rows = torch.arange(len(hidden), device=hidden.device)[:, None].expand_as(targets)
        packed_rows = pack_padded_sequence(
            token_rows, lengths.cpu(), batch_first=True, enforce_sorted=False
        ).data
        step_nll = F.cross_entropy(logits, packed_targets, reduction="none")
        token_nll = torch.zeros(len(hidden), device=hidden.device)
        token_nll.scatter_add_(0, packed_rows, step_nll)
        return HeadLoss(
            loss=token_nll.mean(),
            token_nll=token_nll,
            byte_lengths=lengths - 1,
            peak_logits_bytes=logits.numel() * logits.element_size(),
        )

    @torch.no_grad()
    def greedy_bytes(self, hidden: torch.Tensor, codec: TokenByteCodec) -> list[bytes]:
        hidden = hidden.reshape(-1, hidden.shape[-1])
        state = self.initial(hidden).unsqueeze(0)
        previous = torch.full((len(hidden),), BOS, device=hidden.device, dtype=torch.long)
        done = torch.zeros(len(hidden), device=hidden.device, dtype=torch.bool)
        values: list[list[int]] = [[] for _ in range(len(hidden))]
        for _ in range(self.max_bytes + 1):
            output, state = self.gru(self.byte_embedding(previous)[:, None, :], state)
            predicted = self.classifier(output[:, 0, :]).argmax(dim=-1)
            for row, value in enumerate(predicted.cpu().tolist()):
                if not bool(done[row]) and value != EOS and len(values[row]) < self.max_bytes:
                    values[row].append(int(value))
            just_done = predicted.eq(EOS)
            done = done | just_done
            if bool(done.all()):
                break
            previous = torch.where(done, torch.full_like(predicted, EOS), predicted)
        return [bytes(row) for row in values]

    @torch.no_grad()
    def beam_bytes_one(self, hidden: torch.Tensor, width: int) -> list[bytes]:
        if hidden.ndim != 1:
            raise ValueError("beam_bytes_one expects one hidden vector")
        initial = self.initial(hidden[None, :]).unsqueeze(0)
        beams: list[tuple[float, tuple[int, ...], int, torch.Tensor, bool]] = [
            (0.0, tuple(), BOS, initial, False)
        ]
        for _ in range(self.max_bytes + 1):
            candidates: list[tuple[float, tuple[int, ...], int, torch.Tensor, bool]] = []
            for score, values, previous, state, done in beams:
                if done:
                    candidates.append((score, values, previous, state, done))
                    continue
                prev = torch.tensor([previous], device=hidden.device)
                output, next_state = self.gru(self.byte_embedding(prev)[:, None, :], state)
                log_probs = F.log_softmax(self.classifier(output[:, 0, :])[0], dim=-1)
                top = torch.topk(log_probs, width)
                for log_p, value in zip(top.values.tolist(), top.indices.tolist()):
                    is_done = value == EOS
                    new_values = values if is_done else (*values, int(value))
                    if len(new_values) > self.max_bytes:
                        is_done = True
                        new_values = new_values[: self.max_bytes]
                    candidates.append(
                        (score + float(log_p), new_values, int(value), next_state.clone(), is_done)
                    )
            candidates.sort(key=lambda item: item[0], reverse=True)
            beams = candidates[:width]
            if all(item[4] for item in beams):
                break
        return [bytes(item[1]) for item in beams]

    @torch.no_grad()
    def topk_bytes(
        self, hidden: torch.Tensor, codec: TokenByteCodec, width: int
    ) -> list[list[bytes]]:
        hidden = hidden.reshape(-1, hidden.shape[-1])
        return [self.beam_bytes_one(row, width) for row in hidden]


def make_head(
    name: str,
    d_model: int,
    vocab_size: int,
    byte_embedding_dim: int = 64,
    decoder_hidden_dim: int = 128,
    parallel_hidden_dim: int = 128,
    max_bytes: int = 128,
) -> nn.Module:
    if name == "vocabulary":
        return VocabularyHead(d_model, vocab_size)
    if name == "parallel_byte":
        return ParallelByteHead(d_model, parallel_hidden_dim, max_bytes)
    if name == "autoregressive_byte":
        return AutoregressiveByteHead(
            d_model, byte_embedding_dim, decoder_hidden_dim, max_bytes
        )
    raise ValueError(f"unknown head: {name}")


def parameter_count(module: nn.Module) -> int:
    return sum(parameter.numel() for parameter in module.parameters() if parameter.requires_grad)


def relative_noise(hidden: torch.Tensor, sigma: float, generator: torch.Generator) -> torch.Tensor:
    if sigma == 0:
        return hidden
    rms = hidden.square().mean(dim=-1, keepdim=True).sqrt().clamp_min(1e-8)
    noise = torch.randn(hidden.shape, generator=generator, device=hidden.device)
    return hidden + noise * rms * sigma

