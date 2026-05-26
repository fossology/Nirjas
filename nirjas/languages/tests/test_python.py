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

from nirjas.languages import python


class PythonTest(unittest.TestCase):
    """
    Test cases for Python language.
    :ivar testfile: Location of test file
    """

    testfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), "python_fixture.py")

    def setUp(self):
        self.result = python.pythonExtractor(self.testfile)

    def test_returns_scan_output(self):
        """pythonExtractor returns an object with the expected attributes."""
        out = self.result
        self.assertIsNotNone(out.filename)
        self.assertIsNotNone(out.lang)
        self.assertIsNotNone(out.total_lines)
        self.assertIsNotNone(out.total_lines_of_comments)
        self.assertIsNotNone(out.blank_lines)
        self.assertIsInstance(out.single_line_comment, list)
        self.assertIsInstance(out.cont_single_line_comment, list)
        self.assertIsInstance(out.multi_line_comment, list)

    def test_language_is_python(self):
        self.assertEqual(self.result.lang, "Python")

    def test_filename(self):
        self.assertEqual(self.result.filename, "python_fixture.py")

    def test_total_lines(self):
        self.assertEqual(self.result.total_lines, 17)

    def test_blank_lines(self):
        self.assertEqual(self.result.blank_lines, 4)

    def test_total_lines_of_comments(self):
        # 1 (line 2) + 2 (lines 4-5) + 4 (lines 7-10) + 1 (line 13) = 8
        self.assertEqual(self.result.total_lines_of_comments, 8)

    def test_sloc(self):
        out = self.result.get_dict()
        self.assertEqual(out["metadata"]["sloc"], 5)

    def test_single_line_count(self):
        # Line 2 + line 13 (single-line triple-quoted string)
        self.assertEqual(len(self.result.single_line_comment), 2)

    def test_single_line_hash_comment(self):
        comment = self.result.single_line_comment[0]
        self.assertEqual(comment.line_number, 2)
        self.assertEqual(comment.comment, "# Single standalone comment")

    def test_single_line_triple_quote_docstring(self):
        comment = self.result.single_line_comment[1]
        self.assertEqual(comment.line_number, 13)
        self.assertEqual(comment.comment, '"""A single-line docstring"""')

    def test_cont_single_line_count(self):
        self.assertEqual(len(self.result.cont_single_line_comment), 1)

    def test_cont_single_line_span(self):
        group = self.result.cont_single_line_comment[0]
        self.assertEqual(group.start_line, 4)
        self.assertEqual(group.end_line, 5)

    def test_cont_single_line_text(self):
        group = self.result.cont_single_line_comment[0]
        self.assertIn("Consecutive comment A", group.comment)
        self.assertIn("Consecutive comment B", group.comment)

    def test_multi_line_count(self):
        self.assertEqual(len(self.result.multi_line_comment), 1)

    def test_multi_line_span(self):
        docstring = self.result.multi_line_comment[0]
        self.assertEqual(docstring.start_line, 7)
        self.assertEqual(docstring.end_line, 10)

    def test_multi_line_text(self):
        docstring = self.result.multi_line_comment[0]
        self.assertIn("Multi-line docstring", docstring.comment)
        self.assertIn('"""', docstring.comment)

    def test_hash_inside_string_is_not_comment(self):
        """Line 16 y = "# not a comment" must not produce an extra comment."""
        all_line_numbers = [
            *[c.line_number for c in self.result.single_line_comment],
            *[c.start_line for c in self.result.cont_single_line_comment],
            *[c.start_line for c in self.result.multi_line_comment],
        ]
        self.assertNotIn(16, all_line_numbers)

    def test_get_dict_structure(self):
        d = self.result.get_dict()
        self.assertIn("metadata", d)
        self.assertIn("single_line_comment", d)
        self.assertIn("cont_single_line_comment", d)
        self.assertIn("multi_line_comment", d)
        meta = d["metadata"]
        for key in ("filename", "lang", "total_lines", "total_lines_of_comments", "blank_lines", "sloc"):
            self.assertIn(key, meta)

    def test_Source(self):
        """pythonSource creates a new file with comments stripped."""
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            name = tmp.name
        try:
            newfile = python.pythonSource(self.testfile, name)
            self.assertTrue(os.path.exists(newfile))
        finally:
            if os.path.exists(name):
                os.unlink(name)
