from __future__ import annotations

import math

import torch
from torch import nn


class K32Encoder(nn.Module):
    """Original K32 position-byte codec followed by its learned projection.

    The fixed one-hot Kronecker code is implemented sparsely: every active
    (position, byte) coordinate gathers one row from the 8192 x d projection.
    """

    def __init__(self, vocab: list[str], d_model: int, max_bytes: int = 32) -> None:
        super().__init__()
        self.max_bytes = max_bytes
        self.d_model = d_model
        byte_rows = torch.zeros((len(vocab), max_bytes), dtype=torch.long)
        lengths = torch.zeros(len(vocab), dtype=torch.long)
        full_lengths = torch.zeros(len(vocab), dtype=torch.long)
        for token_id, token in enumerate(vocab):
            raw = token.encode("utf-8")
            full_lengths[token_id] = len(raw)
            truncated = raw[:max_bytes]
            lengths[token_id] = len(truncated)
            if truncated:
                byte_rows[token_id, : len(truncated)] = torch.tensor(list(truncated))
        self.register_buffer("token_bytes", byte_rows, persistent=True)
        self.register_buffer("token_lengths", lengths, persistent=True)
        self.register_buffer("full_token_lengths", full_lengths, persistent=True)
        self.coordinate_projection = nn.Embedding(max_bytes * 256, d_model)
        nn.init.normal_(self.coordinate_projection.weight, mean=0.0, std=1.0 / math.sqrt(d_model))

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        raw = self.token_bytes[token_ids]
        lengths = self.token_lengths[token_ids]
        positions = torch.arange(self.max_bytes, device=token_ids.device)
        view_shape = (1,) * token_ids.ndim + (self.max_bytes,)
        positions = positions.view(view_shape)
        coordinates = positions * 256 + raw
        values = self.coordinate_projection(coordinates)
        mask = positions < lengths.unsqueeze(-1)
        values = values * mask.unsqueeze(-1)
        scale = torch.sqrt(lengths.clamp_min(1).to(values.dtype)).unsqueeze(-1)
        return values.sum(dim=-2) / scale

    def truncated_mask(self, token_ids: torch.Tensor) -> torch.Tensor:
        return self.full_token_lengths[token_ids] > self.max_bytes

