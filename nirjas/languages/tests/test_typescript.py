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
from nirjas.languages import typescript
from nirjas.binder import readSingleLine, readMultiLineDiff


class TSTest(unittest.TestCase):
    testfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), "TestFiles/textcomment.ts")

    def test_output(self):
        regex = r'''(?<![pst]:)\/\/\s*(.*)'''
        self.syntax_start = "/*"
        self.syntax_end = '*/'
        sign = '//'
        comment_single = typescript.readSingleLine(self.testfile, regex, sign)
        comment_multiline = typescript.readMultiLineDiff(self.testfile, self.syntax_start, self.syntax_end)
        comment_contSingleline = typescript.contSingleLines(comment_single)
        self.assertTrue(comment_single)
        self.assertTrue(comment_multiline)
        self.assertTrue(comment_contSingleline)

    def test_outputFormat(self):
        regex = r'''(?<![pst]:)\/\/\s*(.*)'''
        self.syntax_start = "/*"
        self.syntax_end = '*/'
        sign = '//'
        expected = typescript.typescriptExtractor(self.testfile).get_dict()
        comment_single = readSingleLine(self.testfile, regex, sign)
        comment_multiline = readMultiLineDiff(self.testfile, self.syntax_start, self.syntax_end)
        comment_contSingleline = typescript.contSingleLines(comment_single)
        file = self.testfile.split("/")
        output = {
        "metadata": {
        "filename": file[-1],
        "lang": "TypeScript",
        "total_lines": comment_single[1],
        "total_lines_of_comments": comment_single[3] + comment_multiline[3],
        "blank_lines": comment_single[2],
        "sloc": comment_single[1] - (comment_single[3] + comment_multiline[3] + comment_single[2])
        },
        "single_line_comment": [],
        "cont_single_line_comment": [],
        "multi_line_comment": []
        }

        if comment_contSingleline:
            comment_single = comment_contSingleline[0]

        for i in comment_single[0]:
            output['single_line_comment'].append({"line_number":i[0], "comment": i[1]})

        for idx, i in enumerate(comment_contSingleline[1]):
            output['cont_single_line_comment'].append({"start_line": comment_contSingleline[1][idx], "end_line": comment_contSingleline[2][idx], "comment": comment_contSingleline[3][idx]})

        try:
            for idx, i in enumerate(comment_multiline[0]):
                output['multi_line_comment'].append({"start_line": comment_multiline[0][idx], "end_line": comment_multiline[1][idx], "comment": comment_multiline[2][idx]})
        except:
            pass

        self.assertEqual(output, expected)

    def test_Source(self):
        name = "source.txt"
        newfile = typescript.typescriptSource(self.testfile, name)

        self.assertTrue(newfile)
