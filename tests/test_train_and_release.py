#!/usr/bin/env python3
"""Unit tests for the gate train-and-release helpers.

SPDX-License-Identifier: LGPL-2.1

Pure standard-library tests: stub pipe returns plain lists; the heavy
train/push paths are not exercised here.
"""
import importlib.util
import unittest
from pathlib import Path

# Load the script as a module (scripts/ is not an importable package).
_SPEC = importlib.util.spec_from_file_location(
    "train_and_release",
    Path(__file__).resolve().parents[1] / "scripts" / "train_and_release.py",
)
assert _SPEC and _SPEC.loader
tar = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(tar)


class _StubPipe:
    def __init__(self, proba):
        self.classes_ = [0, 1]
        self._proba = proba

    def predict_proba(self, texts):
        assert len(texts) == len(self._proba)
        return self._proba


class EvaluateTest(unittest.TestCase):
    def test_recall_and_fpr_at_threshold(self):
        # 2 positives (dataset label 0), 2 negatives (label 1).
        rows = [
            {"text": "pos1", "label": 0},
            {"text": "pos2", "label": 0},
            {"text": "neg1", "label": 1},
            {"text": "neg2", "label": 1},
        ]
        # license_related (col 1) probas: pos1=0.9, pos2=0.1, neg1=0.3, neg2=0.05
        pipe = _StubPipe([[0.1, 0.9], [0.9, 0.1], [0.7, 0.3], [0.95, 0.05]])
        m = tar.evaluate(pipe, rows, threshold=0.20)
        self.assertEqual(m["license_recall"], 0.5)        # only pos1 > 0.20
        self.assertEqual(m["false_positive_rate"], 0.5)   # only neg1 > 0.20
        self.assertEqual(m["test_size"], 4)


class GateTest(unittest.TestCase):
    def test_passes_gate(self):
        good = {"license_recall": 0.995, "false_positive_rate": 0.02}
        self.assertTrue(tar.passes_gate(good, min_recall=0.99, max_fpr=0.05))
        self.assertFalse(tar.passes_gate(good, min_recall=0.999, max_fpr=0.05))  # recall too low
        bad_fpr = {"license_recall": 0.995, "false_positive_rate": 0.09}
        self.assertFalse(tar.passes_gate(bad_fpr, min_recall=0.99, max_fpr=0.05))


class MetaTest(unittest.TestCase):
    def test_build_gate_meta_shape(self):
        m = {"license_recall": 0.9952, "false_positive_rate": 0.0227}
        meta = tar.build_gate_meta(m, threshold=0.20, base_model="minishlab/potion-base-32M")
        self.assertEqual(meta["license_threshold"], 0.20)
        self.assertEqual(meta["base_model"], "minishlab/potion-base-32M")
        self.assertEqual(meta["test_license_recall"], 0.9952)
        self.assertEqual(meta["test_false_positive_rate"], 0.0227)


if __name__ == "__main__":
    unittest.main()
