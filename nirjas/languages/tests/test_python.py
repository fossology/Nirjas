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
from nirjas.languages import python
from nirjas.binder import readSingleLine, readMultiLineSame, contSingleLines


class PythonTest(unittest.TestCase):
    """
    Test cases for Python language.
    :ivar testfile: Location of test file
    """

    testfile = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "TestFiles/textcomment.py"
    )

    def test_output(self):
        """
        Check for the scan correctness.
        """
        regex = r"""(?<!["'`])#+\s*(.*)"""
        syntax_single = "'''"
        syntax_double = '"""'
        comment_multi_single = readMultiLineSame(self.testfile, syntax_single)
        comment_single = readSingleLine(self.testfile, regex)
        comment_multi_double = readMultiLineSame(self.testfile, syntax_double)
        comment_contSingleline = contSingleLines(comment_single)
        self.assertTrue(comment_single)
        self.assertTrue(comment_multi_single)
        self.assertTrue(comment_multi_double)
        self.assertTrue(comment_contSingleline)

    def test_outputFormat(self):
        """
        Check for the output format correctness.
        """
        regex = r"""(?<!["'`])#+\s*(.*)"""
        syntax_single = "'''"
        syntax_double = '"""'
        expected = python.pythonExtractor(self.testfile).get_dict()
        comment_single = readSingleLine(self.testfile, regex)
        comment_multi_single = readMultiLineSame(self.testfile, syntax_single)
        comment_multi_double = readMultiLineSame(self.testfile, syntax_double)
        comment_contSingleline = contSingleLines(comment_single)
        file = self.testfile.split("/")
        blank_lines_in_comment = comment_multi_single[4] + comment_multi_double[4]
        output = {
            "metadata": {
                "filename": file[-1],
                "lang": "Python",
                "total_lines": comment_single[1],
                "total_lines_of_comments": comment_single[3] + comment_multi_single[3] + comment_multi_double[3],
                "blank_lines": comment_single[2],
                "blank_lines_in_comment": blank_lines_in_comment,
                "blank_lines_outside_comment": comment_single[2] - blank_lines_in_comment,
                "sloc": comment_single[1] - (
                    comment_single[3] + comment_multi_single[3] + comment_multi_double[3] + (comment_single[2] - blank_lines_in_comment)
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

        self.assertEqual(output, expected)

    def test_blank_in_multiline(self):
        """
        Check for correctness when a multiline comment contains a blank line.
        """
        multiline_blank_file = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "TestFiles/multiline_blank.py"
        )
        # Create it if it doesn't exist for some reason
        if not os.path.exists(os.path.dirname(multiline_blank_file)):
            os.makedirs(os.path.dirname(multiline_blank_file))
        with open(multiline_blank_file, "w", encoding="utf-8") as f:
            f.write('"""\nTesting multiline\n\nwith blank lines\n"""\nprint("Hello")\n# comment')
        
        # total=7, comment=5(multi)+1(single)=6, blank=1, blank_in_comment=1, sloc=7-(6+0)=1
        expected_sloc = 1
        result = python.pythonExtractor(multiline_blank_file).get_dict()
        self.assertEqual(result["metadata"]["sloc"], expected_sloc)
        self.assertEqual(result["metadata"]["total_lines_of_comments"], 6)
        self.assertEqual(result["metadata"]["blank_lines"], 1)

    def test_Source(self):
        """
        Test the source code extraction.
        Call the source function and check if new file exists.
        """
        name = "source.txt"
        newfile = python.pythonSource(self.testfile, name)

        self.assertTrue(newfile)
