#!/usr/bin/env python3
"""Runtime inference for the Nirjas recall-first license gate.

SPDX-License-Identifier: LGPL-2.1

The gate answers "is this text actual license text worth routing to Atarashi?".
It is a recall-first binary classifier: label 1 == license_related. The decision
uses a recall-first threshold (0.20), NOT argmax-0.5 — missing a license is the
costly error; a false positive just wastes an Atarashi call.

Inference is torch-free (model2vec static embedding + skops sklearn head). The
model is loaded from HF Hub and cached by huggingface_hub on first use.

    from nirjas.gate import load_gate, classify
    pipe, th = load_gate()                       # downloads rycerzes/nirjas-gate
    classify(pipe, ["// SPDX-License-Identifier: MIT"], th)  # -> [True]
"""
import json
from pathlib import Path
from typing import Iterable

DEFAULT_REPO_ID = "rycerzes/nirjas-gate"
DEFAULT_THRESHOLD = 0.20  # recall-first operating point; see gate_meta.json


def _require_model2vec():
    """Return model2vec's StaticModelPipeline, or a helpful error if the extra is missing."""
    try:
        from model2vec.inference import StaticModelPipeline
    except ImportError as e:  # pragma: no cover - trivial guard
        raise ImportError(
            "The Nirjas gate needs the 'gate' extra. Install with: "
            "pip install 'nirjas[gate]'"
        ) from e
    return StaticModelPipeline


def _download_meta(repo_id: str) -> str:
    """Download gate_meta.json from the Hub repo; return its local path."""
    from huggingface_hub import hf_hub_download

    return hf_hub_download(repo_id, "gate_meta.json")


def load_gate(repo_id: str = DEFAULT_REPO_ID):
    """Load the published gate pipeline and its recall-first threshold from HF Hub."""
    StaticModelPipeline = _require_model2vec()
    pipe = StaticModelPipeline.from_pretrained(repo_id)
    meta = json.loads(Path(_download_meta(repo_id)).read_text())
    return pipe, meta["license_threshold"]


def classify(pipe, texts: Iterable[str], threshold: float = DEFAULT_THRESHOLD) -> list[bool]:
    """Return, per text, whether it is license-related at the recall-first threshold."""
    texts = list(texts)
    if not texts:
        return []
    pos = list(pipe.classes_).index(1)  # 1 == license_related (dataset label 0)
    proba = pipe.predict_proba(texts)
    return [bool(row[pos] > threshold) for row in proba]
