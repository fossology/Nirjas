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

import unittest
import os
from nirjas.languages import css
from nirjas.binder import readMultiLineDiff


class CssTest(unittest.TestCase):
    """
    Test cases for CSS language.
    :ivar testfile: Location of test file
    """

    testfile = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "TestFiles/textcomment.css"
    )

    def test_output(self):
        """
        Check for the scan correctness.
        """
        syntax_start = "/*"
        syntax_end = "*/"
        comment_multiline = readMultiLineDiff(self.testfile, syntax_start, syntax_end)

        self.assertTrue(comment_multiline)

    def test_outputFormat(self):
        """
        Check for the output format correctness.
        """
        syntax_start = "/*"
        syntax_end = "*/"
        expected = css.cssExtractor(self.testfile).get_dict()
        comment_multiline = readMultiLineDiff(self.testfile, syntax_start, syntax_end)
        file = self.testfile.split("/")
        output = {
            "metadata": {
                "filename": file[-1],
                "lang": "CSS",
                "total_lines": comment_multiline[4],
                "total_lines_of_comments": comment_multiline[3],
                "blank_lines": comment_multiline[5],
                "sloc": comment_multiline[4] - (comment_multiline[3] + comment_multiline[5]),
            },
            "single_line_comment": [],
            "cont_single_line_comment": [],
            "multi_line_comment": [],
        }
        if comment_multiline:
            for idx, _ in enumerate(comment_multiline[0]):
                output["multi_line_comment"].append(
                    {
                        "start_line": comment_multiline[0][idx],
                        "end_line": comment_multiline[1][idx],
                        "comment": comment_multiline[2][idx],
                    }
                )

        self.assertEqual(output, expected)

    def test_Source(self):
        """
        Test the source code extraction.
        Call the source function and check if new file exists.
        """
        name = "source.txt"
        newfile = css.cssSource(self.testfile, name)

        self.assertTrue(newfile)
