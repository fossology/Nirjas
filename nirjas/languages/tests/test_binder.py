#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
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

import os
import tempfile
import unittest

from nirjas.binder import contSingleLines, readSingleLine
from nirjas.languages import java, python


class ContSingleLinesTest(unittest.TestCase):
    """
    Test cases for merging consecutive single line comments.
    Comments that trail code on the same line must never be merged
    into a cont_single_line_comment block.
    """

    def _makeFile(self, source, suffix):
        fd, path = tempfile.mkstemp(suffix=suffix, text=True)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(source)
        self.addCleanup(os.remove, path)
        return path

    def test_consecutiveFullLineCommentsAreMerged(self):
        """
        Consecutive comments that occupy their whole line are merged.
        """
        source = (
            "public class Test {\n"
            "    // first line of block\n"
            "    // second line of block\n"
            "    public void foo() {}\n"
            "}\n"
        )
        result = java.javaExtractor(self._makeFile(source, ".java")).get_dict()
        self.assertEqual(result["single_line_comment"], [])
        self.assertEqual(
            result["cont_single_line_comment"],
            [
                {
                    "start_line": 2,
                    "end_line": 3,
                    "comment": " first line of block second line of block",
                }
            ],
        )

    def test_trailingCommentsAreNotMerged(self):
        """
        Comments trailing code on consecutive lines stay independent.
        """
        source = (
            "public class Test {\n"
            "    public void foo() {\n"
            "        int x = 5; // set x to five\n"
            "        int y = 6; // set y to six\n"
            "    }\n"
            "}\n"
        )
        result = java.javaExtractor(self._makeFile(source, ".java")).get_dict()
        self.assertEqual(result["cont_single_line_comment"], [])
        self.assertEqual(
            result["single_line_comment"],
            [
                {"line_number": 3, "comment": "set x to five"},
                {"line_number": 4, "comment": "set y to six"},
            ],
        )

    def test_fullLineCommentIsNotMergedWithTrailingComment(self):
        """
        A full-line comment followed by a trailing comment on the next
        line must not become a continuation block.
        """
        source = (
            "public class Test {\n"
            "    // explains the next line\n"
            "    int x = 5; // set x to five\n"
            "}\n"
        )
        result = java.javaExtractor(self._makeFile(source, ".java")).get_dict()
        self.assertEqual(result["cont_single_line_comment"], [])
        self.assertEqual(
            result["single_line_comment"],
            [
                {"line_number": 2, "comment": "explains the next line"},
                {"line_number": 3, "comment": "set x to five"},
            ],
        )

    def test_trailingCommentBetweenFullLineComments(self):
        """
        A trailing comment must split the runs around it; full-line
        comments after it can still form their own block.
        """
        source = (
            "int x = 5; // trailing\n"
            "// block line one\n"
            "// block line two\n"
        )
        result = java.javaExtractor(self._makeFile(source, ".java")).get_dict()
        self.assertEqual(
            result["single_line_comment"],
            [{"line_number": 1, "comment": "trailing"}],
        )
        self.assertEqual(
            result["cont_single_line_comment"],
            [
                {
                    "start_line": 2,
                    "end_line": 3,
                    "comment": " block line one block line two",
                }
            ],
        )

    def test_trailingHashCommentsAreNotMerged(self):
        """
        The fix applies to every language using readSingleLine.
        """
        source = (
            "x = 5  # set x to five\n"
            "y = 6  # set y to six\n"
        )
        result = python.pythonExtractor(self._makeFile(source, ".py")).get_dict()
        self.assertEqual(result["cont_single_line_comment"], [])
        self.assertEqual(
            result["single_line_comment"],
            [
                {"line_number": 1, "comment": "set x to five"},
                {"line_number": 2, "comment": "set y to six"},
            ],
        )

    def test_readSingleLineReportsFullLineFlag(self):
        """
        readSingleLine flags whether a comment occupies its whole line.
        """
        source = (
            "// full line\n"
            "int x = 5; // trailing\n"
        )
        regex = r"""(?<![pst'"`]:)\/\/\s*(.*)"""
        content, _, _, _ = readSingleLine(self._makeFile(source, ".java"), regex)
        self.assertEqual(
            content,
            [[1, "full line", True], [2, "trailing", False]],
        )

    def test_contSingleLinesAcceptsEntriesWithoutFlag(self):
        """
        Two-element entries from older callers keep the old behaviour.
        """
        data = ([[1, "first"], [2, "second"], [4, "alone"]], 5, 0, 3)
        remaining, start_line, end_line, output = contSingleLines(data)
        self.assertEqual(remaining[0], [[4, "alone"]])
        self.assertEqual(start_line, [1])
        self.assertEqual(end_line, [2])
        self.assertEqual(output, [" first second"])
