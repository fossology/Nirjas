#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tier 2: real-world source files, asserted against full goldens.

Three files per supported language, vendored verbatim from permissively
licensed upstreams at pinned commits. Real code exercises constructs no
hand-written fixture thinks to include: licence header blocks, doc-comment
conventions, heredocs, embedded languages, long files with hundreds of
comments.

These carry the same exact goldens as the hand-written tier. Nobody reads a
600-line golden top to bottom, but that is not how goldens are used: you read
the *diff* when behaviour changes, and a three-line diff in a large golden is
perfectly reviewable. The invariants run alongside, because a golden
regenerated from broken code would otherwise enshrine the breakage.

Every vendored file carries an ``.ABOUT`` sidecar recording origin, pinned
commit and licence, following the AboutCode convention ScanCode uses for its
own vendored test data. Nirjas is a licence-compliance tool; unattributed
third-party files in the tree are not acceptable.

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

CORPUS = golden.iter_corpus()

#: Fields an .ABOUT sidecar must carry for the vendored file to be traceable.
REQUIRED_ABOUT_FIELDS = (
    "about_resource",
    "download_url",
    "license_expression",
    "copyright",
)

#: Copyleft terms we deliberately keep out of the corpus. Vendoring these into
#: an LGPL-2.1 tree is a licence question a test suite should not decide on its
#: own, so the guard fails loudly rather than letting one drift in.
DISALLOWED_LICENSES = ("gpl-2.0", "gpl-3.0", "agpl-3.0", "lgpl-3.0")

pytestmark = pytest.mark.corpus


def _about_for(path: Path) -> Path:
    return path.with_name(path.name + ".ABOUT")


def _parse_about(path: Path) -> dict[str, str]:
    """Read the ``key: value`` pairs of an .ABOUT file.

    Deliberately minimal rather than a YAML dependency: continuation lines are
    indented, which is all the format needs here.
    """

    fields: dict[str, str] = {}
    current: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        if raw_line[:1].isspace() and current:
            fields[current] += " " + raw_line.strip()
            continue
        key, separator, value = raw_line.partition(":")
        if separator:
            current = key.strip()
            fields[current] = value.strip()
    return fields


def test_corpus_is_discovered():
    """A suite that silently collects nothing would pass while testing nothing."""

    assert CORPUS, f"no corpus files found under {golden.CORPUS_ROOT}"


def test_every_supported_language_has_corpus_files():
    """The point of this tier is real-world coverage for *every* language."""

    covered = {path.parent.name for path in CORPUS}
    missing = sorted(set(EXTRACTORS) - covered)
    assert not missing, f"languages with no real-world corpus file: {missing}"


def test_corpus_golden_stems_unique():
    golden.assert_golden_stems_unique(CORPUS)


@pytest.mark.parametrize("path", CORPUS, ids=golden.fixture_id)
def test_corpus_scan_output_matches_golden(path: Path):
    language = nirjas_name_from_path(str(path))
    actual = EXTRACTORS[language](str(path)).get_dict()

    # Invariants first: true by construction, so they fail on a golden that was
    # regenerated from broken behaviour.
    contract.assert_scan_output_contract(actual, str(path))
    golden.assert_scan_matches_golden(path, actual)


@pytest.mark.parametrize("path", CORPUS, ids=golden.fixture_id)
def test_corpus_stripped_source_matches_golden(path: Path, tmp_path: Path):
    language = nirjas_name_from_path(str(path))
    if language not in SOURCES:
        # `text` has an extractor but no source stripper: there is no code to
        # keep in a plain-text file. EXTRACTORS has 26 entries, SOURCES 25.
        pytest.skip(f"{language} has no source extractor")

    destination = tmp_path / "source.txt"

    returned = SOURCES[language](str(path), str(destination))
    assert returned == str(destination), "source extractor must return its output path"

    with destination.open("r", encoding="utf-8", newline="") as handle:
        actual = handle.read()
    golden.assert_source_matches_golden(path, actual)


@pytest.mark.parametrize("path", CORPUS, ids=golden.fixture_id)
def test_corpus_file_has_provenance(path: Path):
    about_file = _about_for(path)
    assert about_file.is_file(), (
        f"vendored file {path.name} has no {about_file.name}; record its origin "
        "and licence before committing it"
    )

    fields = _parse_about(about_file)
    missing = [field for field in REQUIRED_ABOUT_FIELDS if not fields.get(field)]
    assert not missing, f"{about_file.name} is missing required fields: {missing}"

    assert fields["about_resource"] == path.name, (
        f"{about_file.name} describes '{fields['about_resource']}' "
        f"but sits beside '{path.name}'"
    )

    # A bare branch URL silently changes meaning over time; pin to a commit.
    download_url = fields["download_url"]
    assert "/blob/main/" not in download_url and "/blob/master/" not in download_url, (
        f"{about_file.name} download_url must pin a commit, not a branch"
    )

    declared = fields["license_expression"].strip().lower()
    assert declared not in DISALLOWED_LICENSES, (
        f"{about_file.name} declares '{declared}', which is deliberately kept "
        "out of the corpus; pick a permissively licensed upstream instead"
    )
