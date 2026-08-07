#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Golden-file discovery and (re)generation for the Nirjas test suite.

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
import os
from pathlib import Path
from typing import Any

#: Set this to any truthy value to rewrite golden files from current behavior
#: instead of asserting against them, e.g. ``NIRJAS_REGEN_FIXTURES=1 pytest``.
REGEN_ENV_VAR = "NIRJAS_REGEN_FIXTURES"

#: Extraction output golden, sitting next to its fixture.
SCAN_GOLDEN_SUFFIX = ".expected.json"

#: Stripped-source golden, kept as plain text so diffs stay readable.
SOURCE_GOLDEN_SUFFIX = ".expected.src"

_GOLDEN_SUFFIXES = (SCAN_GOLDEN_SUFFIX, SOURCE_GOLDEN_SUFFIX)

DATA_ROOT = Path(__file__).resolve().parent.parent / "data"

#: Tier 1: small hand-written files we own, asserted against exact goldens.
FIXTURE_ROOT = DATA_ROOT / "fixtures"

#: Tier 2: vendored real-world files, asserted against invariants only.
CORPUS_ROOT = DATA_ROOT / "corpus"

#: Provenance sidecars for vendored corpus files; never scanned as input.
CORPUS_METADATA_SUFFIXES = (".ABOUT", ".LICENSE", ".NOTICE")


def regen_requested() -> bool:
    """True when the caller asked for golden files to be rewritten."""

    value = os.environ.get(REGEN_ENV_VAR, "").strip().lower()
    return value not in ("", "0", "no", "false", "off")


def scan_golden_for(fixture: Path) -> Path:
    """Path of the extraction golden belonging to ``fixture``."""

    return fixture.with_name(fixture.stem + SCAN_GOLDEN_SUFFIX)


def source_golden_for(fixture: Path) -> Path:
    """Path of the stripped-source golden belonging to ``fixture``."""

    return fixture.with_name(fixture.stem + SOURCE_GOLDEN_SUFFIX)


def _is_input_file(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.name.endswith(_GOLDEN_SUFFIXES):
        return False
    if path.suffix in CORPUS_METADATA_SUFFIXES:
        return False
    if path.name.startswith("."):
        return False
    # Never treat build residue or hidden directories as scannable input.
    return not any(
        part == "__pycache__" or part.startswith(".") for part in path.parent.parts
    )


def iter_fixtures() -> list[Path]:
    """Every tier-1 fixture, sorted for stable test ordering and ids."""

    if not FIXTURE_ROOT.is_dir():
        return []
    return sorted(path for path in FIXTURE_ROOT.rglob("*") if _is_input_file(path))


def iter_corpus() -> list[Path]:
    """Every tier-2 vendored corpus file, sorted for stable ordering."""

    if not CORPUS_ROOT.is_dir():
        return []
    return sorted(path for path in CORPUS_ROOT.rglob("*") if _is_input_file(path))


def fixture_id(path: Path | None) -> str:
    """Readable pytest id, e.g. ``python/hash_in_string.py``."""

    # Empty-parametrize placeholders pass None; keep them collectable.
    if not isinstance(path, Path):
        return "unavailable"

    root = FIXTURE_ROOT if FIXTURE_ROOT in path.parents else CORPUS_ROOT
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.name


def load_json_golden(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_golden(path: Path, payload: Any) -> None:
    # Trailing newline keeps the files POSIX-clean and diff-friendly.
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False)
    path.write_text(serialized + "\n", encoding="utf-8")


def _regen_hint(missing: Path) -> str:
    return (
        f"no golden recorded at {missing.name}; review the input then create it "
        f"with `{REGEN_ENV_VAR}=1 pytest`"
    )


def assert_scan_matches_golden(input_file: Path, actual: Any) -> None:
    """Compare extractor output against its golden, or rewrite it in regen mode."""

    golden_file = scan_golden_for(input_file)
    if regen_requested():
        write_json_golden(golden_file, actual)

    assert golden_file.is_file(), _regen_hint(golden_file)
    assert actual == load_json_golden(golden_file)


def assert_source_matches_golden(input_file: Path, actual: str) -> None:
    """Compare stripped source against its golden, or rewrite it in regen mode."""

    golden_file = source_golden_for(input_file)
    if regen_requested():
        write_text_golden(golden_file, actual)

    assert golden_file.is_file(), _regen_hint(golden_file)
    assert actual == load_text_golden(golden_file)


def assert_golden_stems_unique(inputs: list[Path]) -> None:
    """Goldens key off the stem, so `a.cc` and `a.cpp` in one dir would clash."""

    seen: dict[Path, Path] = {}
    for input_file in inputs:
        key = scan_golden_for(input_file)
        assert key not in seen, (
            f"{input_file} and {seen[key]} would share the golden {key.name}; "
            "rename one of them"
        )
        seen[key] = input_file


def load_text_golden(path: Path) -> str:
    # newline="" so recorded line endings survive the round trip verbatim.
    # Path.read_text() only accepts newline from 3.13, and we target 3.10.
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_text_golden(path: Path, payload: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(payload)
