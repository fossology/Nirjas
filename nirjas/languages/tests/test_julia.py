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
import unittest

from nirjas.binder import (contSingleLines, readMultiLineDiff,
                           readMultiLineSame, readSingleLine)
from nirjas.languages import julia


class JuliaTest(unittest.TestCase):
    """
    Test cases for Julia language.
    :ivar testfile: Location of test file
    """

    testfile = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "TestFiles/textcomment.jl"
    )

    def test_output(self):
        """
        Check for the scan correctness.
        """
        regex = r"""(?<!["'`])#+\s*(.*)"""
        syntax_single = "'''"
        syntax_double = '"""'
        syntax_start = "#="
        syntax_end = "=#"
        comment_multi_single = readMultiLineSame(self.testfile, syntax_single)
        comment_single = readSingleLine(self.testfile, regex)
        comment_multi_double = readMultiLineSame(self.testfile, syntax_double)
        comment_multi_hashEqual = readMultiLineDiff(
            self.testfile, syntax_start, syntax_end
        )
        comment_contSingleline = contSingleLines(comment_single)
        self.assertTrue(comment_single)
        self.assertTrue(comment_multi_single)
        self.assertTrue(comment_multi_double)
        self.assertTrue(comment_multi_hashEqual)
        self.assertTrue(comment_contSingleline)

    def test_outputFormat(self):
        """
        Check for the output format correctness.
        """
        regex = r"""(?<!["'`])#+\s*(.*)"""
        syntax_single = "'''"
        syntax_double = '"""'
        syntax_start = "#="
        syntax_end = "=#"
        expected = julia.juliaExtractor(self.testfile).get_dict()
        comment_single = readSingleLine(self.testfile, regex)
        comment_multi_single = readMultiLineSame(self.testfile, syntax_single)
        comment_multi_double = readMultiLineSame(self.testfile, syntax_double)
        comment_multi_hashEqual = readMultiLineDiff(
            self.testfile, syntax_start, syntax_end
        )
        comment_contSingleline = contSingleLines(comment_single)
        file = self.testfile.split("/")
        output = {
            "metadata": {
                "filename": file[-1],
                "lang": "Julia",
                "total_lines": comment_single[1],
                "total_lines_of_comments": comment_single[3]
                + comment_multi_single[3]
                + comment_multi_double[3]
                + comment_multi_hashEqual[3],
                "blank_lines": comment_single[2],
                "sloc": comment_single[1]
                - (
                    comment_single[3]
                    + comment_multi_single[3]
                    + comment_multi_double[3]
                    + comment_multi_hashEqual[3]
                    + comment_single[2]
                ),
            },
            "single_line_comment": [],
            "cont_single_line_comment": [],
            "multi_line_comment": [],
        }

        if comment_contSingleline:
            comment_single = comment_contSingleline[0]

        if comment_single:
            for i in comment_single[0]:
                output["single_line_comment"].append(
                    {"line_number": i[0], "comment": i[1]}
                )

        if comment_contSingleline:
            for idx, _ in enumerate(comment_contSingleline[1]):
                output["cont_single_line_comment"].append(
                    {
                        "start_line": comment_contSingleline[1][idx],
                        "end_line": comment_contSingleline[2][idx],
                        "comment": comment_contSingleline[3][idx],
                    }
                )

        if comment_multi_single:
            for idx, _ in enumerate(comment_multi_single[0]):
                output["multi_line_comment"].append(
                    {
                        "start_line": comment_multi_single[0][idx],
                        "end_line": comment_multi_single[1][idx],
                        "comment": comment_multi_single[2][idx],
                    }
                )

        if comment_multi_double:
            for idx, _ in enumerate(comment_multi_double[0]):
                output["multi_line_comment"].append(
                    {
                        "start_line": comment_multi_double[0][idx],
                        "end_line": comment_multi_double[1][idx],
                        "comment": comment_multi_double[2][idx],
                    }
                )

        if comment_multi_hashEqual:
            for idx, _ in enumerate(comment_multi_hashEqual[0]):
                output["multi_line_comment"].append(
                    {
                        "start_line": comment_multi_hashEqual[0][idx],
                        "end_line": comment_multi_hashEqual[1][idx],
                        "comment": comment_multi_hashEqual[2][idx],
                    }
                )

        self.assertEqual(output, expected)

    def test_Source(self):
        """
        Test the source code extraction.
        Call the source function and check if new file exists.
        """
        name = "source.txt"
        newfile = julia.juliaSource(self.testfile, name)

        self.assertTrue(newfile)
