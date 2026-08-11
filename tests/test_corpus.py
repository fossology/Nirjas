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

Origin, pinned commit and licence for the whole corpus live in one manifest,
``tests/data/corpus/PROVENANCE.json``, grouped by upstream. Nirjas is a
licence-compliance tool, so unattributed third-party files in the tree are not
acceptable -- but attribution is a property of the nine upstreams, not of the
78 files, and recording it per upstream keeps a commit bump to a one-line diff.

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

import json
import re
from pathlib import Path

import pytest

from helpers import contract, golden
from nirjas.language_registry import nirjas_name_from_path
from nirjas.main import EXTRACTORS, SOURCES

CORPUS = golden.iter_corpus()

#: Fields an upstream entry must carry for its files to be traceable.
REQUIRED_UPSTREAM_FIELDS = (
    "homepage_url",
    "commit",
    "license_expression",
    "copyright",
)

#: Copyleft terms we deliberately keep out of the corpus. Vendoring these into
#: an LGPL-2.1 tree is a licence question a test suite should not decide on its
#: own, so the guard fails loudly rather than letting one drift in.
DISALLOWED_LICENSES = ("gpl-2.0", "gpl-3.0", "agpl-3.0", "lgpl-3.0")

#: A full 40-character SHA. A tag or branch silently changes meaning over time,
#: which defeats the point of recording where a file came from.
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")

pytestmark = pytest.mark.corpus


def _load_manifest() -> dict[str, dict]:
    """Upstream entries from PROVENANCE.json, keyed by ``owner/repo``."""

    if not golden.CORPUS_MANIFEST.is_file():
        return {}
    payload = json.loads(golden.CORPUS_MANIFEST.read_text(encoding="utf-8"))
    return payload.get("upstreams", {})


UPSTREAMS = _load_manifest()

#: Corpus-relative path -> the upstream that owns it, flattened once so the
#: per-file checks stay a lookup rather than a scan.
OWNER_OF = {
    corpus_path: repo
    for repo, upstream in UPSTREAMS.items()
    for corpus_path in upstream.get("files", {})
}


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


def test_provenance_manifest_exists():
    """Without it every check below would pass by having nothing to check."""

    assert UPSTREAMS, (
        f"no upstream entries in {golden.CORPUS_MANIFEST}; vendored files must "
        "record where they came from"
    )


@pytest.mark.parametrize("repo", sorted(UPSTREAMS), ids=lambda repo: repo)
def test_upstream_entry_is_complete(repo: str):
    upstream = UPSTREAMS[repo]

    missing = [field for field in REQUIRED_UPSTREAM_FIELDS if not upstream.get(field)]
    assert not missing, f"upstream '{repo}' is missing required fields: {missing}"

    assert upstream["homepage_url"] == f"https://github.com/{repo}", (
        f"upstream '{repo}' has homepage_url '{upstream['homepage_url']}', which "
        "does not match its key; download_url is derived from both"
    )

    assert COMMIT_SHA.match(upstream["commit"]), (
        f"upstream '{repo}' pins '{upstream['commit']}'; a full 40-character "
        "commit SHA is required, because a tag or branch can be moved"
    )

    declared = upstream["license_expression"].strip().lower()
    assert declared not in DISALLOWED_LICENSES, (
        f"upstream '{repo}' declares '{declared}', which is deliberately kept "
        "out of the corpus; pick a permissively licensed upstream instead"
    )

    assert upstream.get("files"), f"upstream '{repo}' claims no files; drop it"


def test_manifest_and_corpus_agree_exactly():
    """Neither an unattributed file nor a stale entry may survive.

    One manifest replaces 78 sidecars, which trades a missing-file failure mode
    for a drifting-index one: deleting a corpus file no longer deletes its
    record. This is the check that buys that back.
    """

    on_disk = {golden.fixture_id(path) for path in CORPUS}
    recorded = set(OWNER_OF)

    unattributed = sorted(on_disk - recorded)
    assert not unattributed, (
        f"vendored files with no entry in {golden.CORPUS_MANIFEST.name}: "
        f"{unattributed}; record origin and licence before committing them"
    )

    orphaned = sorted(recorded - on_disk)
    assert not orphaned, (
        f"{golden.CORPUS_MANIFEST.name} describes files that are not in the "
        f"corpus: {orphaned}; remove the stale entries"
    )


@pytest.mark.parametrize("path", CORPUS, ids=golden.fixture_id)
def test_corpus_file_has_provenance(path: Path):
    corpus_path = golden.fixture_id(path)
    repo = OWNER_OF.get(corpus_path)
    assert repo, f"{corpus_path} has no upstream entry"

    upstream_path = UPSTREAMS[repo]["files"][corpus_path]
    assert upstream_path and not upstream_path.startswith("/"), (
        f"{corpus_path} records upstream path '{upstream_path}', which is not a "
        "repository-relative path"
    )

    # The manifest stores the pieces rather than the URL, so nothing can drift
    # out of step with the commit pin above; this is the shape it resolves to.
    download_url = (
        f"{UPSTREAMS[repo]['homepage_url']}/blob/"
        f"{UPSTREAMS[repo]['commit']}/{upstream_path}"
    )
    assert "/blob/main/" not in download_url and "/blob/master/" not in download_url
