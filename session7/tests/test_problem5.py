from __future__ import annotations

import math

import pytest
import torch

from session7.src.config import ExperimentConfig
from session7.src.data import load_data_bundle
from session7.src.decoders import (
    AutoregressiveByteHead,
    ParallelByteHead,
    TokenByteCodec,
    VocabularyHead,
    parameter_count,
)
from session7.src.encoders import K32Encoder
from session7.src.transformer import ReverseKroneckerLM, initial_backbone_state


@pytest.fixture(scope="module")
def data():
    return load_data_bundle()


@pytest.fixture(scope="module")
def codec(data):
    return TokenByteCodec(data.vocab, 128)


def test_codec_roundtrips_every_vocabulary_item(data, codec):
    assert codec.roundtrip_ok()
    assert max(len(value) for value in codec.sequences) == 115
    assert len(codec.known) == len(data.vocab)


def test_teacher_forcing_has_bos_bytes_and_eos(codec):
    ids = torch.tensor([0, 1, 9999])
    inputs, targets, lengths = codec.teacher_forcing_tensors(ids, torch.device("cpu"))
    for row, token_id in enumerate(ids.tolist()):
        seq = codec.sequences[token_id]
        length = len(seq) + 1
        assert int(lengths[row]) == length
        assert int(inputs[row, 0]) == 257
        assert targets[row, : len(seq)].tolist() == list(seq)
        assert int(targets[row, len(seq)]) == 256


def test_k32_is_deterministic_and_normalized():
    vocab = ["a", "aa", "b", "x" * 33, "x" * 32 + "y"]
    torch.manual_seed(3)
    encoder = K32Encoder(vocab, d_model=16)
    first = encoder(torch.tensor([0, 1, 2]))
    second = encoder(torch.tensor([0, 1, 2]))
    assert torch.equal(first, second)
    assert torch.isfinite(first).all()
    # Same 32-byte prefix is the documented K32 collision.
    long = encoder(torch.tensor([3, 4]))
    assert torch.equal(long[0], long[1])
    assert encoder.truncated_mask(torch.tensor([0, 3])).tolist() == [False, True]


def test_k32_position_byte_coordinate_mapping():
    encoder = K32Encoder(["a", "aa"], d_model=4)
    with torch.no_grad():
        encoder.coordinate_projection.weight.zero_()
        encoder.coordinate_projection.weight[97] = torch.tensor([1.0, 0.0, 0.0, 0.0])
        encoder.coordinate_projection.weight[256 + 97] = torch.tensor([0.0, 1.0, 0.0, 0.0])
    result = encoder(torch.tensor([0, 1]))
    assert torch.allclose(result[0], torch.tensor([1.0, 0.0, 0.0, 0.0]))
    assert torch.allclose(
        result[1], torch.tensor([1.0, 1.0, 0.0, 0.0]) / math.sqrt(2)
    )


@pytest.mark.parametrize("head_name", ["vocabulary", "parallel", "autoregressive"])
def test_heads_produce_finite_token_losses(codec, head_name):
    hidden = torch.randn(8, 32, requires_grad=True)
    ids = torch.tensor([0, 1, 2, 3, 4, 5, 100, 9999])
    if head_name == "vocabulary":
        head = VocabularyHead(32, 10_000)
    elif head_name == "parallel":
        head = ParallelByteHead(32, hidden_dim=24, max_bytes=128)
    else:
        head = AutoregressiveByteHead(32, byte_embedding_dim=16, hidden_dim=24)
    output = head.loss(hidden, ids, codec)
    assert output.token_nll.shape == (8,)
    assert output.byte_lengths.shape == (8,)
    assert output.peak_logits_bytes > 0
    assert torch.isfinite(output.loss)
    output.loss.backward()
    assert hidden.grad is not None
    assert torch.isfinite(hidden.grad).all()


def test_output_parameter_reduction(codec):
    standard = VocabularyHead(128, 10_000)
    parallel = ParallelByteHead(128, 128, 128)
    autoregressive = AutoregressiveByteHead(128, 64, 128, 128)
    assert parameter_count(standard) / parameter_count(autoregressive) >= 8
    assert parameter_count(standard) / parameter_count(parallel) >= 15


def test_parallel_decoder_can_overfit_tiny_mapping():
    vocab = ["a", "b", "cat", "न"]
    codec = TokenByteCodec(vocab, 16)
    hidden = torch.eye(4)
    ids = torch.arange(4)
    head = ParallelByteHead(4, hidden_dim=32, max_bytes=16)
    optimizer = torch.optim.Adam(head.parameters(), lr=0.05)
    for _ in range(100):
        optimizer.zero_grad()
        output = head.loss(hidden, ids, codec)
        output.loss.backward()
        optimizer.step()
    assert head.greedy_bytes(hidden, codec) == [value.encode("utf-8") for value in vocab]


def test_autoregressive_decoder_can_overfit_and_beam_terminates():
    vocab = ["a", "b", "cat", "न"]
    codec = TokenByteCodec(vocab, 16)
    hidden = torch.eye(4)
    ids = torch.arange(4)
    head = AutoregressiveByteHead(4, byte_embedding_dim=16, hidden_dim=32, max_bytes=16)
    optimizer = torch.optim.Adam(head.parameters(), lr=0.05)
    for _ in range(120):
        optimizer.zero_grad()
        output = head.loss(hidden, ids, codec)
        output.loss.backward()
        optimizer.step()
    assert head.greedy_bytes(hidden, codec) == [value.encode("utf-8") for value in vocab]
    beams = head.beam_bytes_one(hidden[0], width=3)
    assert beams
    assert len(beams) <= 3
    assert all(len(value) <= 16 for value in beams)


def test_tiny_model_uses_identical_backbone_state(data, codec):
    config = ExperimentConfig.smoke()
    state = initial_backbone_state(data.vocab, config, seed=7)
    vocab_model = ReverseKroneckerLM(data.vocab, config, "vocabulary", state)
    byte_model = ReverseKroneckerLM(data.vocab, config, "autoregressive_byte", state)
    for key, value in vocab_model.backbone.state_dict().items():
        assert torch.equal(value, byte_model.backbone.state_dict()[key])
    ids = torch.randint(0, len(data.vocab), (2, config.context_length))
    targets = torch.randint(0, len(data.vocab), (2, config.context_length))
    loss = byte_model.loss(ids, targets, codec).loss
    assert torch.isfinite(loss)

