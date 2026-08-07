#!/usr/bin/env python3
"""Unit tests for the Nirjas gate inference module.

SPDX-License-Identifier: LGPL-2.1

Pure standard-library tests: stub pipes return plain lists, and the two
external-dependency helpers are patched, so no numpy / model2vec /
huggingface_hub import happens at test time.
"""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from nirjas.gate import inference


class _StubPipe:
    """Mimics model2vec StaticModelPipeline: classes_ + predict_proba."""

    def __init__(self, proba):
        self.classes_ = [0, 1]  # 1 == license_related
        self._proba = proba  # list of [p_not_license, p_license] rows

    def predict_proba(self, texts):
        assert len(texts) == len(self._proba)
        return self._proba


class ClassifyTest(unittest.TestCase):
    def test_applies_recall_first_threshold(self):
        # license_related (col 1) probas: 0.10, 0.25, 0.90
        pipe = _StubPipe([[0.90, 0.10], [0.75, 0.25], [0.10, 0.90]])
        out = inference.classify(pipe, ["a", "b", "c"], threshold=0.20)
        self.assertEqual(out, [False, True, True])  # 0.10<=0.20 False; 0.25,0.90>0.20 True

    def test_empty_returns_empty(self):
        pipe = _StubPipe([])
        self.assertEqual(inference.classify(pipe, [], threshold=0.20), [])


class LoadGateTest(unittest.TestCase):
    def test_reads_threshold_from_meta(self):
        # Patch both external-dependency helpers so no network / model2vec /
        # huggingface_hub is touched.
        with tempfile.TemporaryDirectory() as td:
            meta_file = Path(td) / "gate_meta.json"
            meta_file.write_text(json.dumps({"license_threshold": 0.2}))

            captured = {}

            class _FakePipeline:
                @staticmethod
                def from_pretrained(repo_id):
                    captured["repo_id"] = repo_id
                    return _StubPipe([])

            with mock.patch.object(inference, "_require_model2vec", return_value=_FakePipeline), \
                 mock.patch.object(inference, "_download_meta", return_value=str(meta_file)):
                pipe, threshold = inference.load_gate("rycerzes/nirjas-gate")

        self.assertEqual(threshold, 0.2)
        self.assertEqual(captured["repo_id"], "rycerzes/nirjas-gate")
        self.assertIsInstance(pipe, _StubPipe)


if __name__ == "__main__":
    unittest.main()
