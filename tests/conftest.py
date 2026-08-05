#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pytest configuration for the Nirjas test suite.

SPDX-License-Identifier: LGPL-2.1
"""

from __future__ import annotations

from helpers import golden

#: Test data is input, never test code. Vendored corpus files include real
#: upstream test suites with names like `test_immutable_exception.py`, which
#: pytest would otherwise import and run. Paths are relative to this conftest.
collect_ignore = ["data"]


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "corpus: invariant checks against vendored real-world files (tier 2)",
    )


def pytest_report_header(config):
    """Make regeneration mode impossible to miss in the run header."""

    if golden.regen_requested():
        return (
            f"nirjas: {golden.REGEN_ENV_VAR} is set - golden files will be "
            "REWRITTEN from current behaviour, not asserted against"
        )
    return None
