#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tier 1: exact golden assertions over hand-written fixtures.

Every fixture under ``tests/data/fixtures`` is scanned with the extractor its
extension maps to, and both the structured output and the stripped source are
compared byte-for-byte against committed goldens. Regenerate with::

    NIRJAS_REGEN_FIXTURES=1 pytest tests/test_golden.py

Copyright (C) 2026  Swapnil Dutta (swapnil@rycerz.es)

SPDX-License-Identifier: LGPL-2.1

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

from __future__ import annotations

from pathlib import Path

import pytest

from helpers import contract, golden
from nirjas.language_registry import nirjas_name_from_path
from nirjas.main import EXTRACTORS, SOURCES

FIXTURES = golden.iter_fixtures()


def test_fixtures_are_discovered():
    """A suite that silently collects nothing would pass while testing nothing."""

    assert FIXTURES, f"no fixtures found under {golden.FIXTURE_ROOT}"


def test_golden_names_do_not_collide():
    golden.assert_golden_stems_unique(FIXTURES)


def test_no_orphaned_goldens():
    """Catch goldens left behind when a fixture is renamed or removed."""

    live = {golden.scan_golden_for(f) for f in FIXTURES}
    live |= {golden.source_golden_for(f) for f in FIXTURES}

    orphans = [
        path
        for path in sorted(golden.FIXTURE_ROOT.rglob("*"))
        if path.is_file()
        and path.name.endswith((golden.SCAN_GOLDEN_SUFFIX, golden.SOURCE_GOLDEN_SUFFIX))
        and path not in live
    ]
    assert not orphans, f"goldens with no matching fixture: {orphans}"


@pytest.mark.parametrize("fixture", FIXTURES, ids=golden.fixture_id)
def test_scan_output_matches_golden(fixture: Path):
    language = nirjas_name_from_path(str(fixture))
    actual = EXTRACTORS[language](str(fixture)).get_dict()

    # Invariants run first. They are true by construction, so they fail on a
    # golden that was regenerated from broken behaviour.
    contract.assert_scan_output_contract(actual, str(fixture))

    golden.assert_scan_matches_golden(fixture, actual)


@pytest.mark.parametrize("fixture", FIXTURES, ids=golden.fixture_id)
def test_stripped_source_matches_golden(fixture: Path, tmp_path: Path):
    language = nirjas_name_from_path(str(fixture))
    if language not in SOURCES:
        # `text` has an extractor but no source stripper: there is no code to
        # keep in a plain-text file. EXTRACTORS has 26 entries, SOURCES 25.
        pytest.skip(f"{language} has no source extractor")

    destination = tmp_path / "source.txt"

    returned = SOURCES[language](str(fixture), str(destination))
    assert returned == str(destination), "source extractor must return its output path"
    assert destination.is_file(), "source extractor must write its output file"

    with destination.open("r", encoding="utf-8", newline="") as handle:
        actual = handle.read()

    golden.assert_source_matches_golden(fixture, actual)
