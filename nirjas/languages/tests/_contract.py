#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared helpers for language extractor contract tests.

Copyright (C) 2020  Ayush Bhardwaj (classicayush@gmail.com),
Kaushlendra Pratap (kaushlendrapratap.9837@gmail.com)
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
import tempfile
from collections.abc import Callable


def _count_lines(file_path: str) -> int:
    with open(file_path, encoding="utf-8", errors="replace") as source_file:
        return sum(1 for _ in source_file)


def _count_blank_lines(file_path: str) -> int:
    with open(file_path, encoding="utf-8", errors="replace") as source_file:
        return sum(1 for line in source_file if line.strip() == "")


def _blank_line_numbers(file_path: str) -> set[int]:
    with open(file_path, encoding="utf-8", errors="replace") as source_file:
        return {
            line_number
            for line_number, line in enumerate(source_file, start=1)
            if line.strip() == ""
        }


def _comment_line_numbers(scan_output: dict) -> set[int]:
    """Distinct source lines carrying a comment, per the reported spans."""

    comment_lines = {
        entry["line_number"] for entry in scan_output["single_line_comment"]
    }

    for section in ["cont_single_line_comment", "multi_line_comment"]:
        for entry in scan_output[section]:
            comment_lines.update(range(entry["start_line"], entry["end_line"] + 1))

    return comment_lines


def assert_scan_output_contract(
    testcase,
    scan_output: dict,
    file_path: str,
    language_name: str,
) -> None:
    """Validate schema + metadata invariants for extractor output."""

    testcase.assertIsInstance(scan_output, dict)

    metadata = scan_output.get("metadata")
    testcase.assertIsInstance(metadata, dict)
    if not isinstance(metadata, dict):
        raise AssertionError("metadata must be a dictionary")

    total_lines = _count_lines(file_path)
    blank_lines = _count_blank_lines(file_path)

    testcase.assertEqual(metadata.get("filename"), os.path.basename(file_path))
    testcase.assertEqual(metadata.get("lang"), language_name)
    testcase.assertEqual(metadata.get("total_lines"), total_lines)
    testcase.assertEqual(metadata.get("blank_lines"), blank_lines)

    for section in [
        "single_line_comment",
        "cont_single_line_comment",
        "multi_line_comment",
    ]:
        testcase.assertIn(section, scan_output)
        testcase.assertIsInstance(scan_output[section], list)

    for single_line_comment in scan_output["single_line_comment"]:
        testcase.assertIn("line_number", single_line_comment)
        testcase.assertIn("comment", single_line_comment)
        testcase.assertGreaterEqual(single_line_comment["line_number"], 1)
        testcase.assertLessEqual(single_line_comment["line_number"], total_lines)

    for contiguous_comment in scan_output["cont_single_line_comment"]:
        testcase.assertIn("start_line", contiguous_comment)
        testcase.assertIn("end_line", contiguous_comment)
        testcase.assertIn("comment", contiguous_comment)
        testcase.assertLessEqual(contiguous_comment["start_line"], contiguous_comment["end_line"])
        testcase.assertGreaterEqual(contiguous_comment["start_line"], 1)
        testcase.assertLessEqual(contiguous_comment["end_line"], total_lines)

    for multi_line_comment in scan_output["multi_line_comment"]:
        testcase.assertIn("start_line", multi_line_comment)
        testcase.assertIn("end_line", multi_line_comment)
        testcase.assertIn("comment", multi_line_comment)
        testcase.assertLessEqual(multi_line_comment["start_line"], multi_line_comment["end_line"])
        testcase.assertGreaterEqual(multi_line_comment["start_line"], 1)
        testcase.assertLessEqual(multi_line_comment["end_line"], total_lines)

    comment_lines = _comment_line_numbers(scan_output)
    metadata_comment_lines = metadata.get("total_lines_of_comments")
    testcase.assertIsInstance(metadata_comment_lines, int)
    if not isinstance(metadata_comment_lines, int):
        raise AssertionError("total_lines_of_comments must be an integer")

    sloc = metadata.get("sloc")
    testcase.assertIsInstance(sloc, int)
    if not isinstance(sloc, int):
        raise AssertionError("sloc must be an integer")

    # Every line is blank, comment, or code and never more than one of those,
    # which is the convention `cloc` uses. So the buckets have to add back up.
    testcase.assertEqual(
        metadata_comment_lines + blank_lines + sloc,
        total_lines,
        "blank + comment + sloc must account for every line exactly once",
    )
    testcase.assertGreaterEqual(sloc, 0)

    # Comment lines are the subset of comment-carrying lines that hold nothing
    # else, so they can never outnumber the lines the spans touch.
    blank_line_numbers = _blank_line_numbers(file_path)
    testcase.assertLessEqual(
        metadata_comment_lines,
        len(comment_lines - blank_line_numbers),
    )


def assert_source_extractor_contract(
    testcase,
    source_extractor: Callable[[str, str], str],
    source_file: str,
) -> None:
    """Validate source extraction API contract."""

    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = os.path.join(temp_dir, "source.txt")
        returned_path = source_extractor(source_file, output_file)

        testcase.assertEqual(returned_path, output_file)
        testcase.assertTrue(os.path.exists(output_file))
