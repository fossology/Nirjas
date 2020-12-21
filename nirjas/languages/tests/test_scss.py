'''
Copyright (C) 2020  Aman Dwivedi (aman.dwivedi5@gmail.com)

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
'''

import unittest
import os
from nirjas.languages import scss
from nirjas.binder import readSingleLine, readMultiLineDiff


class ScssTest(unittest.TestCase):
    testfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), "TestFiles/textcomment.scss")

    def test_output(self):
        regex1 = r'''(?<!\/)\/\/(?!\/)\s*(.*)'''
        regex2 = r'''\/\/\/\s*(.*)'''
        self.syntax_start = "/*"
        self.syntax_end = '*/'
        sign1 = '//'
        sign2 = '///'
        comment_single_doubleSlash = scss.readSingleLine(self.testfile, regex1, sign1)
        comment_single_tripleSlash = scss.readSingleLine(self.testfile, regex2, sign2)
        comment_multiline = scss.readMultiLineDiff(self.testfile, self.syntax_start, self.syntax_end)
        comment_contSingleline1 = scss.contSingleLines(comment_single_doubleSlash)
        comment_contSingleline2 = scss.contSingleLines(comment_single_tripleSlash)
        self.assertTrue(comment_single_doubleSlash)
        self.assertTrue(comment_single_tripleSlash)
        self.assertTrue(comment_multiline)
        self.assertTrue(comment_contSingleline1)
        self.assertTrue(comment_contSingleline2)

    def test_outputFormat(self):
        regex1 = r'''(?<!\/)\/\/(?!\/)\s*(.*)'''
        regex2 = r'''\/\/\/\s*(.*)'''
        self.syntax_start = "/*"
        self.syntax_end = '*/'
        sign1 = '//'
        sign2 = '///'
        expected = scss.scssExtractor(self.testfile).get_dict()
        comment_single_doubleSlash = scss.readSingleLine(self.testfile, regex1, sign1)
        comment_single_tripleSlash = scss.readSingleLine(self.testfile, regex2, sign2)
        comment_multiline = scss.readMultiLineDiff(self.testfile, self.syntax_start, self.syntax_end)
        comment_contSingleline1 = scss.contSingleLines(comment_single_doubleSlash)
        comment_contSingleline2 = scss.contSingleLines(comment_single_tripleSlash)
        file = self.testfile.split("/")
        output = {
        "metadata": {
        "filename": file[-1],
        "lang": "Scss",
        "total_lines": comment_single_doubleSlash[1],
        "total_lines_of_comments": comment_single_doubleSlash[3] + comment_single_tripleSlash[3] + comment_multiline[3],
        "blank_lines": comment_single_doubleSlash[2],
        "sloc": comment_single_doubleSlash[1] - (comment_single_doubleSlash[3] + comment_single_tripleSlash[3] + comment_multiline[3] + comment_single_doubleSlash[2])
        },
        "single_line_comment": [],
        "cont_single_line_comment": [],
        "multi_line_comment": []
        }

        if comment_contSingleline1:
            comment_single_doubleSlash = comment_contSingleline1[0]

        if comment_contSingleline2:
            comment_single_tripleSlash = comment_contSingleline2[0]

        if comment_single_doubleSlash:
            for i in comment_single_doubleSlash[0]:
                output['single_line_comment'].append({"line_number":i[0], "comment": i[1]})

        if comment_single_tripleSlash:
            for i in comment_single_tripleSlash[0]:
                output['single_line_comment'].append({"line_number":i[0], "comment": i[1]})

        if comment_contSingleline1:
            for idx, i in enumerate(comment_contSingleline1[1]):
                output['cont_single_line_comment'].append({"start_line": comment_contSingleline1[1][idx], "end_line": comment_contSingleline1[2][idx], "comment": comment_contSingleline1[3][idx]})

        if comment_contSingleline2:
            for idx, i in enumerate(comment_contSingleline2[1]):
                output['cont_single_line_comment'].append({"start_line": comment_contSingleline2[1][idx], "end_line": comment_contSingleline2[2][idx], "comment": comment_contSingleline2[3][idx]})

        if comment_multiline:
            try:
                for idx, i in enumerate(comment_multiline[0]):
                    output['multi_line_comment'].append({"start_line": comment_multiline[0][idx], "end_line": comment_multiline[1][idx], "comment": comment_multiline[2][idx]})
            except:
                pass

        self.assertEqual(output, expected)

    def test_Source(self):
        name = "source.txt"
        newfile = scss.scssSource(self.testfile, name)

        self.assertTrue(newfile)
