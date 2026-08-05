#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Behaviour-independent invariants every extractor result must satisfy.

These hold for any input in any language, so they stay meaningful even for
vendored corpus files whose exact expected output nobody has hand-checked.
They also guard the golden files: a golden regenerated from buggy code would
happily enshrine the bug, but it cannot satisfy invariants that are true by
construction.

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

import os

SPAN_SECTIONS = ("cont_single_line_comment", "multi_line_comment")
ALL_SECTIONS = ("single_line_comment",) + SPAN_SECTIONS


def _read_lines(file_path: str) -> list[str]:
    with open(file_path, encoding="utf-8", errors="replace") as source_file:
        return source_file.readlines()


def blank_line_numbers(file_path: str) -> set[int]:
    return {
        line_number
        for line_number, line in enumerate(_read_lines(file_path), start=1)
        if line.strip() == ""
    }


def comment_line_numbers(scan_output: dict) -> set[int]:
    """Distinct source lines touched by any reported comment span."""

    lines = {entry["line_number"] for entry in scan_output["single_line_comment"]}
    for section in SPAN_SECTIONS:
        for entry in scan_output[section]:
            lines.update(range(entry["start_line"], entry["end_line"] + 1))
    return lines


def assert_scan_output_contract(
    scan_output: dict,
    file_path: str,
    language_name: str | None = None,
) -> None:
    """Validate the output schema and every metadata invariant."""

    assert isinstance(scan_output, dict), "scan output must be a dict"

    metadata = scan_output.get("metadata")
    assert isinstance(metadata, dict), "metadata must be a dict"

    source_lines = _read_lines(file_path)
    total_lines = len(source_lines)
    blank_lines = sum(1 for line in source_lines if line.strip() == "")

    assert metadata.get("filename") == os.path.basename(file_path)
    if language_name is not None:
        assert metadata.get("lang") == language_name
    assert metadata.get("total_lines") == total_lines, "total_lines must match the file"
    assert metadata.get("blank_lines") == blank_lines, "blank_lines must match the file"

    for section in ALL_SECTIONS:
        assert section in scan_output, f"missing section {section}"
        assert isinstance(scan_output[section], list), f"{section} must be a list"

    for entry in scan_output["single_line_comment"]:
        assert "line_number" in entry
        assert "comment" in entry
        assert 1 <= entry["line_number"] <= total_lines, (
            f"single-line comment at {entry['line_number']} outside 1..{total_lines}"
        )

    for section in SPAN_SECTIONS:
        for entry in scan_output[section]:
            assert "start_line" in entry
            assert "end_line" in entry
            assert "comment" in entry
            assert entry["start_line"] <= entry["end_line"], (
                f"{section} span {entry['start_line']}..{entry['end_line']} inverted"
            )
            assert 1 <= entry["start_line"], f"{section} start_line below 1"
            assert entry["end_line"] <= total_lines, (
                f"{section} end_line {entry['end_line']} beyond {total_lines}"
            )

    reported_comment_lines = metadata.get("total_lines_of_comments")
    assert isinstance(reported_comment_lines, int), (
        "total_lines_of_comments must be an integer"
    )

    sloc = metadata.get("sloc")
    assert isinstance(sloc, int), "sloc must be an integer"

    # Every line is blank, comment, or code and never more than one of those,
    # which is the convention `cloc` uses. So the buckets have to add back up.
    assert reported_comment_lines + blank_lines + sloc == total_lines, (
        "blank + comment + sloc must account for every line exactly once: "
        f"{blank_lines} + {reported_comment_lines} + {sloc} != {total_lines}"
    )
    assert sloc >= 0, "sloc cannot be negative"

    # Comment lines are the subset of comment-carrying lines that hold nothing
    # else, so they can never outnumber the lines the spans touch.
    touched = comment_line_numbers(scan_output) - blank_line_numbers(file_path)
    assert reported_comment_lines <= len(touched), (
        f"total_lines_of_comments {reported_comment_lines} exceeds the "
        f"{len(touched)} non-blank lines the reported spans touch"
    )
