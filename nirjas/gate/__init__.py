#!/usr/bin/env python3
"""Nirjas license gate: recall-first classifier in front of Atarashi.

SPDX-License-Identifier: LGPL-2.1
"""
from nirjas.gate.inference import (
    DEFAULT_REPO_ID,
    DEFAULT_THRESHOLD,
    classify,
    load_gate,
)

__all__ = ["load_gate", "classify", "DEFAULT_REPO_ID", "DEFAULT_THRESHOLD"]
