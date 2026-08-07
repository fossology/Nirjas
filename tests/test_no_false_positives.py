#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""No comment token inside a string literal may be reported as a comment.

This is the false-positive class the Tree-Sitter migration exists to remove
(issue #72). Golden files cannot express it on their own: a golden records
whatever the extractor currently does, so a golden regenerated while the bug is
live simply enshrines the bug. This check states the rule independently.

Every fixture places the sentinel phrase below *only* inside string literals,
so the phrase appearing in extracted comment text means a literal leaked in.

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

from helpers import golden
from nirjas.language_registry import nirjas_name_from_path
from nirjas.main import EXTRACTORS

#: Present only inside string literals in every fixture that carries it.
STRING_ONLY_SENTINEL = "not a comment"

#: Present only in genuine comments, so it guards against the inverse mistake
#: of a test passing because nothing at all was extracted.
REAL_COMMENT_SENTINEL = "trailing comment after code"

#: Known false positives awaiting a fix, keyed by fixture id. Keyed per fixture
#: rather than per language, because a language can have one construct that
#: trips and another that does not.
#:
#: Empty, and worth keeping that way. It previously held the Swift single-line
#: string and HTML quoted-attribute cases, both caused by a grammar emitting a
#: comment node directly inside a quoted construct; the
#: QUOTED_PARENT_NODE_KINDS guard in comment_visitor now handles them.
#:
#: Entries use strict xfail, so a fix flips the test to XPASS and fails the run.
#: That failure is the reminder to delete the entry rather than leave a passing
#: test permanently mislabelled as expected-to-fail.
GRAMMAR_FALSE_POSITIVES: set[str] = set()


def _carries_sentinel(fixture: Path) -> bool:
    """Only fixtures built for this check opt in; edge-case fixtures do not."""

    try:
        with fixture.open("r", encoding="utf-8", errors="replace") as handle:
            return STRING_ONLY_SENTINEL in handle.read()
    except OSError:
        return False


def _params():
    for fixture in golden.iter_fixtures():
        if not _carries_sentinel(fixture):
            continue
        fixture_key = golden.fixture_id(fixture)
        marks = []
        if fixture_key in GRAMMAR_FALSE_POSITIVES:
            marks.append(
                pytest.mark.xfail(
                    strict=True,
                    reason=(
                        f"upstream grammar nests a comment node inside a quoted "
                        f"construct in {fixture_key}; needs an ancestor guard in "
                        "collect_comment_spans"
                    ),
                )
            )
        yield pytest.param(fixture, marks=marks)


PARAMS = list(_params())


def test_sentinel_fixtures_exist():
    """Without opted-in fixtures this whole module would cover nothing."""

    assert PARAMS, (
        f"no fixture contains {STRING_ONLY_SENTINEL!r}; the false-positive "
        "check has nothing to assert against"
    )


@pytest.mark.parametrize("fixture", PARAMS, ids=golden.fixture_id)
def test_string_literals_are_not_reported_as_comments(fixture: Path):
    language = nirjas_name_from_path(str(fixture))
    # Bare dict, not dict[str, object]: the section values are heterogeneous
    # lists and get indexed below, matching the convention in helpers.contract.
    scan_output: dict = EXTRACTORS[language](str(fixture)).get_dict()

    extracted = [entry["comment"] for entry in scan_output["single_line_comment"]]
    for section in ("cont_single_line_comment", "multi_line_comment"):
        extracted += [entry["comment"] for entry in scan_output[section]]

    leaked = [text for text in extracted if STRING_ONLY_SENTINEL in text]
    assert not leaked, (
        f"string-literal content reported as a comment in {fixture.name}: {leaked}"
    )

    # Guard the guard: if nothing was extracted at all the check above is vacuous.
    assert any(REAL_COMMENT_SENTINEL in text for text in extracted), (
        f"no genuine comment extracted from {fixture.name}; the false-positive "
        "check above would pass vacuously"
    )
