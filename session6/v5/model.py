from __future__ import annotations

from typing import Any

import torch
from torch import nn

from .data import ByteTokenizer

class TinyCausalLM(nn.Module):
    def __init__(self, vocab_size: int, sequence_length: int, model_config: dict[str, Any]):
        super().__init__()
        width = model_config["d_model"]
        self.token_embedding = nn.Embedding(vocab_size, width)
        self.position_embedding = nn.Embedding(sequence_length, width)
        self.attention = nn.MultiheadAttention(width, model_config["n_heads"], dropout=0.0, batch_first=True)
        self.norm1 = nn.LayerNorm(width)
        self.ffn = nn.Sequential(nn.Linear(width, model_config["ffn_dim"]), nn.GELU(), nn.Linear(model_config["ffn_dim"], width))
        self.norm2 = nn.LayerNorm(width)
        self.lm_head = nn.Linear(width, vocab_size)

    def forward(self, input_ids: torch.Tensor, position_ids: torch.Tensor, attention_allowed: torch.Tensor) -> torch.Tensor:
        hidden = self.token_embedding(input_ids) + self.position_embedding(position_ids)
        attended: list[torch.Tensor] = []
        for batch_index in range(hidden.shape[0]):
            mask = ~attention_allowed[batch_index]
            value, _ = self.attention(
                hidden[batch_index : batch_index + 1],
                hidden[batch_index : batch_index + 1],
                hidden[batch_index : batch_index + 1],
                attn_mask=mask,
                need_weights=False,
            )
            attended.append(value)
        attention_output = torch.cat(attended, dim=0)
        hidden = self.norm1(hidden + attention_output)
        hidden = self.norm2(hidden + self.ffn(hidden))
        return self.lm_head(hidden)


def make_model(config: dict[str, Any], tokenizer: ByteTokenizer) -> TinyCausalLM:
    return TinyCausalLM(tokenizer.vocab_size, config["sequence_length"], config["model"])


def state_dict_cpu(model: nn.Module) -> dict[str, torch.Tensor]:
    return {name: tensor.detach().cpu().clone() for name, tensor in model.state_dict().items()}


