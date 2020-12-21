import unittest
import os
from nirjas.languages import r
from nirjas.binder import readSingleLine


class rTest(unittest.TestCase):
    testfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), "TestFiles/textcomment.R")

    def test_output(self):
        regex = r'''#+\s*(.*)'''
        sign = '#'
        comment_single = r.readSingleLine(self.testfile, regex, sign)
        self.assertTrue(comment_single)

    def test_outputFormat(self):
        regex = r'''#+\s*(.*)'''
        sign = '#'
        expected = r.rExtractor(self.testfile).get_dict()
        comment_single = readSingleLine(self.testfile, regex, sign)
        file = self.testfile.split("/")
        output = {
        "metadata": {
        "filename": file[-1],
        "lang": "R",
        "total_lines": comment_single[1],
        "total_lines_of_comments": comment_single[3],
        "blank_lines": comment_single[2],
        "sloc": comment_single[1] - (comment_single[3] + comment_single[2])
        },
        "single_line_comment": [],
        "cont_single_line_comment": [],
        "multi_line_comment": []
        }
        if comment_single:
            for i in comment_single[0]:
                output['single_line_comment'].append({"line_number":i[0], "comment": i[1]})
        self.assertEqual(output, expected)

    def test_Source(self):
        name = "source.txt"
        newfile = r.rSource(self.testfile, name)

        self.assertTrue(newfile)
