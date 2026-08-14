from __future__ import annotations

import copy

import torch
from torch import nn

from .config import ExperimentConfig
from .decoders import HeadLoss, TokenByteCodec, make_head
from .encoders import K32Encoder


class SharedBackbone(nn.Module):
    """K32 input path plus a small causal Transformer shared by every head."""

    def __init__(self, vocab: list[str], config: ExperimentConfig) -> None:
        super().__init__()
        self.config = config
        self.k32 = K32Encoder(vocab, config.d_model, config.input_max_bytes)
        self.sequence_position = nn.Embedding(config.context_length, config.d_model)
        layer = nn.TransformerEncoderLayer(
            d_model=config.d_model,
            nhead=config.n_heads,
            dim_feedforward=config.ffn_dim,
            dropout=0.0,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.transformer = nn.TransformerEncoder(
            layer, num_layers=config.n_layers, enable_nested_tensor=False
        )
        self.final_norm = nn.LayerNorm(config.d_model)
        mask = torch.triu(
            torch.ones(config.context_length, config.context_length, dtype=torch.bool),
            diagonal=1,
        )
        self.register_buffer("causal_mask", mask, persistent=False)

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        if token_ids.ndim != 2:
            raise ValueError("token_ids must have shape [batch, sequence]")
        sequence = token_ids.shape[1]
        if sequence > self.config.context_length:
            raise ValueError(
                f"sequence {sequence} exceeds context {self.config.context_length}"
            )
        positions = torch.arange(sequence, device=token_ids.device)
        x = self.k32(token_ids) + self.sequence_position(positions)[None, :, :]
        x = self.transformer(x, mask=self.causal_mask[:sequence, :sequence])
        return self.final_norm(x)


class ReverseKroneckerLM(nn.Module):
    def __init__(
        self,
        vocab: list[str],
        config: ExperimentConfig,
        head_name: str,
        backbone_state: dict[str, torch.Tensor] | None = None,
    ) -> None:
        super().__init__()
        self.config = config
        self.head_name = head_name
        self.backbone = SharedBackbone(vocab, config)
        if backbone_state is not None:
            self.backbone.load_state_dict(copy.deepcopy(backbone_state))
        self.head = make_head(
            head_name,
            config.d_model,
            len(vocab),
            config.byte_embedding_dim,
            config.decoder_hidden_dim,
            config.parallel_hidden_dim,
            config.output_max_bytes,
        )

    def hidden(self, input_ids: torch.Tensor) -> torch.Tensor:
        return self.backbone(input_ids)

    def loss(
        self, input_ids: torch.Tensor, target_ids: torch.Tensor, codec: TokenByteCodec
    ) -> HeadLoss:
        hidden = self.hidden(input_ids).reshape(-1, self.config.d_model)
        return self.head.loss(hidden, target_ids.reshape(-1), codec)

    @torch.no_grad()
    def greedy_bytes(self, input_ids: torch.Tensor, codec: TokenByteCodec) -> list[bytes]:
        hidden = self.hidden(input_ids).reshape(-1, self.config.d_model)
        return self.head.greedy_bytes(hidden, codec)


def initial_backbone_state(
    vocab: list[str], config: ExperimentConfig, seed: int
) -> dict[str, torch.Tensor]:
    torch.manual_seed(seed)
    backbone = SharedBackbone(vocab, config)
    return {key: value.detach().clone() for key, value in backbone.state_dict().items()}

