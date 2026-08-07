#!/usr/bin/env python3
"""Train + release the Nirjas recall-first license gate.

SPDX-License-Identifier: LGPL-2.1

Reproduces the gate validated in minerva-dataset-pipeline: a model2vec
classifier on potion-base-32M, recall-first threshold 0.20. Deterministic
(random_seed=0) — retraining yields the same validated gate.

Two modes (mirrors fossology/safaa's train_and_release.py):
  LOCAL  train + eval + quality gate; save artifacts to --output-dir. No push.
  CI     (GITHUB_ACTIONS=true) on gate pass, push the pipeline + gate_meta.json
         to the HF Hub model repo (--repo-id). Needs HF_TOKEN in the env.

    poetry run python scripts/train_and_release.py --output-dir trained_gate
    GITHUB_ACTIONS=true poetry run python scripts/train_and_release.py \
        --repo-id rycerzes/nirjas-gate
"""
import argparse
import json
import logging
import os
import sys
from pathlib import Path

BASE_MODEL = "minishlab/potion-base-32M"
DATASET_REPO = "rycerzes/nirjas-dataset"
MODEL_REPO = "rycerzes/nirjas-gate"
LICENSE_THRESHOLD = 0.20  # recall-first operating point (NOT argmax-0.5)

LOG = logging.getLogger("train_and_release")


def is_ci() -> bool:
    return os.environ.get("GITHUB_ACTIONS") == "true"


def _texts_labels(split):
    """dataset label 0 == license_related -> classifier positive class 1."""
    return list(split["text"]), [1 if lab == 0 else 0 for lab in split["label"]]


def train_gate(dataset_repo: str = DATASET_REPO):
    """Fit the model2vec classifier; return (pipeline, test_split)."""
    from datasets import load_dataset
    from model2vec import StaticModel
    from model2vec.train import StaticModelForClassification

    d = load_dataset(dataset_repo)
    trX, trY = _texts_labels(d["train"])
    vaX, vaY = _texts_labels(d["validation"])

    clf = StaticModelForClassification.from_static_model(
        model=StaticModel.from_pretrained(BASE_MODEL)
    )
    # model2vec's fit stub types labels as str; we use int 0/1, which it accepts
    # at runtime (classes_ come back as ints — matches inference's classes_.index(1)).
    clf.fit(trX, trY, X_val=vaX, y_val=vaY, early_stopping_patience=3, random_seed=0)  # pyright: ignore[reportArgumentType]
    return clf.to_pipeline(), d["test"]


def evaluate(pipe, test_rows, threshold: float = LICENSE_THRESHOLD) -> dict:
    """Recall on license text + false-positive rate at the recall-first threshold.

    test_rows: an iterable of {"text": str, "label": int} in DATASET label
    convention (0 == license_related). Works for a HF split or a list of dicts.
    """
    rows = list(test_rows)
    texts = [r["text"] for r in rows]
    y = [1 if r["label"] == 0 else 0 for r in rows]
    pos = list(pipe.classes_).index(1)
    proba = [row[pos] for row in pipe.predict_proba(texts)]
    pos_i = [i for i, yy in enumerate(y) if yy == 1]
    neg_i = [i for i, yy in enumerate(y) if yy == 0]
    recall = sum(proba[i] > threshold for i in pos_i) / len(pos_i)
    fpr = sum(proba[i] > threshold for i in neg_i) / len(neg_i)
    return {
        "license_recall": round(float(recall), 4),
        "false_positive_rate": round(float(fpr), 4),
        "test_size": len(texts),
    }


def passes_gate(metrics: dict, min_recall: float, max_fpr: float) -> bool:
    return metrics["license_recall"] >= min_recall and metrics["false_positive_rate"] <= max_fpr


def build_gate_meta(metrics: dict, threshold: float, base_model: str) -> dict:
    return {
        "base_model": base_model,
        "license_threshold": threshold,
        "test_license_recall": metrics["license_recall"],
        "test_false_positive_rate": metrics["false_positive_rate"],
        "note": "recall-first gate; label 1 == license_related",
    }


def _save(pipe, meta: dict, output_dir: str):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    pipe.save_pretrained(output_dir)
    (Path(output_dir) / "gate_meta.json").write_text(json.dumps(meta, indent=2))
    (Path(output_dir) / "metrics.json").write_text(json.dumps(meta, indent=2))


def _push(output_dir: str, repo_id: str):
    from huggingface_hub import HfApi  # type: ignore[import-not-found]

    api = HfApi()
    api.create_repo(repo_id, repo_type="model", exist_ok=True)
    api.upload_folder(folder_path=output_dir, repo_id=repo_id, repo_type="model")
    LOG.info("pushed gate -> https://huggingface.co/%s", repo_id)


def main(argv=None):
    p = argparse.ArgumentParser(description="Train + release the Nirjas license gate")
    p.add_argument("--dataset-repo", default=DATASET_REPO)
    p.add_argument("--repo-id", default=MODEL_REPO, help="HF Hub model repo to push to (CI mode)")
    p.add_argument("--output-dir", default="trained_gate")
    p.add_argument("--threshold", type=float, default=LICENSE_THRESHOLD)
    p.add_argument("--min-recall", type=float, default=0.99, help="quality gate: min license recall")
    p.add_argument("--max-fpr", type=float, default=0.05, help="quality gate: max false-positive rate")
    args = p.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    LOG.info("training gate from %s (base=%s)", args.dataset_repo, BASE_MODEL)
    pipe, test = train_gate(args.dataset_repo)
    metrics = evaluate(pipe, test, threshold=args.threshold)
    LOG.info(
        "license recall @ %.2f: %.4f | FPR: %.4f (n=%d)",
        args.threshold, metrics["license_recall"], metrics["false_positive_rate"], metrics["test_size"],
    )

    if not passes_gate(metrics, args.min_recall, args.max_fpr):
        LOG.error(
            "QUALITY GATE FAILED: recall %.4f (need >= %.4f) / FPR %.4f (need <= %.4f). Not saved.",
            metrics["license_recall"], args.min_recall, metrics["false_positive_rate"], args.max_fpr,
        )
        return 1

    meta = build_gate_meta(metrics, args.threshold, BASE_MODEL)
    _save(pipe, meta, args.output_dir)
    LOG.info("saved gate artifacts -> %s/", args.output_dir)

    if is_ci():
        _push(args.output_dir, args.repo_id)
    else:
        LOG.info("local mode: no push. Artifacts in %s/", args.output_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
