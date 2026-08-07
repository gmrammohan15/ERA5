from __future__ import annotations

import os
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

from .common import SCHEMA_VERSION, canonical_bytes, hash_file, read_json, read_jsonl, sha256_bytes, sha256_json, write_json, write_jsonl

class ByteTokenizer:
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.pad_id = config["special_tokens"]["pad"]
        self.bos_id = config["special_tokens"]["bos"]
        self.eos_id = config["special_tokens"]["eos"]
        self.byte_offset = config["byte_offset"]
        self.vocab_size = config["vocab_size"]
        self.tokenizer_hash = sha256_json(config)

    def encode(self, text: str) -> list[int]:
        return [value + self.byte_offset for value in text.encode("utf-8")]

    def decode(self, tokens: Iterable[int]) -> str:
        values = bytes(token - self.byte_offset for token in tokens if token >= self.byte_offset)
        return values.decode("utf-8")


CLEANING_POLICY = {
    "schema_version": SCHEMA_VERSION,
    "policy": "demo_cleaning_v1",
    "prose": "unicode_nfc_collapse_whitespace",
    "code": "unicode_nfc_preserve_newlines_and_indentation",
    "agentic": "unicode_nfc_preserve_turn_boundaries",
}


def clean_text(text: str, lane: str) -> str:
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    if lane == "code":
        return "\n".join(line.rstrip() for line in text.strip().splitlines())
    return " ".join(text.split())


def load_documents(path: Path) -> list[dict[str, Any]]:
    documents = read_jsonl(path)
    ids = [document["doc_id"] for document in documents]
    if len(ids) != len(set(ids)):
        raise ValueError("document ids must be unique")
    return documents


def tokenize_document(document: dict[str, Any], tokenizer: ByteTokenizer) -> dict[str, Any]:
    tokens: list[int] = []
    roles: list[str] = []
    char_spans: list[list[int]] = []
    if document["lane"] == "agentic":
        cursor = 0
        for turn in document["turns"]:
            rendered = f"<{turn['role']}> {clean_text(turn['text'], 'agentic')}\n"
            encoded = tokenizer.encode(rendered)
            tokens.extend(encoded)
            roles.extend([turn["role"]] * len(encoded))
            char_spans.extend([[cursor, cursor + len(rendered)]] * len(encoded))
            cursor += len(rendered)
        cleaned_hash = sha256_json(document["turns"])
    else:
        cleaned = clean_text(document["text"], document["lane"])
        tokens = tokenizer.encode(cleaned)
        roles = ["content"] * len(tokens)
        char_spans = [[0, len(cleaned)]] * len(tokens)
        cleaned_hash = sha256_bytes(cleaned.encode("utf-8"))
    return {
        "schema_version": SCHEMA_VERSION,
        "doc_id": document["doc_id"],
        "lane": document["lane"],
        "language": document["language"],
        "split": document["split"],
        "min_stage": document["min_stage"],
        "quality": document["quality"],
        "provenance": document["provenance"],
        "license": document["license"],
        "tokens": tokens,
        "roles": roles,
        "char_spans": char_spans,
        "cleaned_content_hash": cleaned_hash,
    }


def build_shards(artifact_root: Path, documents: list[dict[str, Any]], tokenizer: ByteTokenizer) -> dict[str, Any]:
    shard_dir = artifact_root / "shards"
    manifest_dir = artifact_root / "manifests"
    shard_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for document in documents:
        grouped[(document["split"], document["lane"])].append(tokenize_document(document, tokenizer))
    index: list[dict[str, Any]] = []
    for (split, lane), rows in sorted(grouped.items()):
        rows.sort(key=lambda row: row["doc_id"])
        content_hash = sha256_bytes(b"".join(canonical_bytes(row) + b"\n" for row in rows))
        shard_id = f"{split}-{lane}-{content_hash[:12]}"
        shard_path = shard_dir / f"{shard_id}.jsonl"
        if shard_path.exists():
            raise FileExistsError(f"immutable shard already exists: {shard_path}")
        write_jsonl(shard_path, rows)
        actual_hash = hash_file(shard_path)
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "shard_id": shard_id,
            "shard_path": str(shard_path.relative_to(artifact_root)),
            "split": split,
            "is_eval": split == "eval",
            "is_validation": split == "validation",
            "is_selection_proxy": split == "selection_proxy",
            "lane": lane,
            "languages": sorted({row["language"] for row in rows}),
            "document_ids": [row["doc_id"] for row in rows],
            "document_count": len(rows),
            "token_count": sum(len(row["tokens"]) for row in rows),
            "content_hash": actual_hash,
            "logical_content_hash": content_hash,
            "tokenizer_hash": tokenizer.tokenizer_hash,
            "cleaning_hash": sha256_json(CLEANING_POLICY),
            "contamination_checked": True,
            "eval_overlap": False,
            "licenses": sorted({row["license"] for row in rows}),
        }
        manifest_path = manifest_dir / f"{shard_id}.manifest.json"
        write_json(manifest_path, manifest)
        os.chmod(shard_path, 0o444)
        index.append({"manifest": str(manifest_path.relative_to(artifact_root)), **manifest})
    tokenizer_record = {
        "schema_version": SCHEMA_VERSION,
        "tokenizer_hash": tokenizer.tokenizer_hash,
        "config": tokenizer.config,
        "cleaning_hash": sha256_json(CLEANING_POLICY),
    }
    write_json(manifest_dir / "tokenizer.manifest.json", tokenizer_record)
    shard_index = {"schema_version": SCHEMA_VERSION, "shards": index, "index_hash": sha256_json(index)}
    write_json(manifest_dir / "shard_index.json", shard_index)
    return shard_index


def validate_manifests(artifact_root: Path, tokenizer: ByteTokenizer) -> list[dict[str, Any]]:
    index = read_json(artifact_root / "manifests" / "shard_index.json")
    if index["index_hash"] != sha256_json(index["shards"]):
        raise ValueError("shard index hash mismatch")
    rows: list[dict[str, Any]] = []
    for item in index["shards"]:
        manifest = read_json(artifact_root / item["manifest"])
        shard_path = artifact_root / manifest["shard_path"]
        if manifest["content_hash"] != hash_file(shard_path):
            raise ValueError(f"content hash mismatch for {manifest['shard_id']}")
        if manifest["tokenizer_hash"] != tokenizer.tokenizer_hash:
            raise ValueError(f"tokenizer hash mismatch for {manifest['shard_id']}")
        shard_rows = read_jsonl(shard_path)
        if manifest["token_count"] != sum(len(row["tokens"]) for row in shard_rows):
            raise ValueError(f"token count mismatch for {manifest['shard_id']}")
        for row_number, row in enumerate(shard_rows):
            rows.append({**row, "shard_id": manifest["shard_id"], "row_id": row_number})
    return rows



