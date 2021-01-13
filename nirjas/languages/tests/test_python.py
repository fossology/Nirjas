import unittest
import os
from nirjas.languages import python
from nirjas.binder import readSingleLine, readMultiLineSame, contSingleLines


class PythonTest(unittest.TestCase):
    testfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), "TestFiles/textcomment.py")

    def test_output(self):
        regex = r'''#+\s*(.*)'''
        self.syntax_single = "'''"
        self.syntax_double = '"""'
        sign = '#'
        comment_multi_single = python.readMultiLineSame(self.testfile, self.syntax_single)
        comment_single = python.readSingleLine(self.testfile, regex, sign)
        comment_multi_double = python.readMultiLineSame(self.testfile, self.syntax_double)
        comment_contSingleline = python.contSingleLines(comment_single)
        self.assertTrue(comment_single)
        self.assertTrue(comment_multi_single)
        self.assertTrue(comment_multi_double)
        self.assertTrue(comment_contSingleline)

    def test_outputFormat(self):
        regex = r'''#+\s*(.*)'''
        self.syntax_single = "'''"
        self.syntax_double = '"""'
        sign = '#'
        expected = python.pythonExtractor(self.testfile).get_dict()
        comment_single = readSingleLine(self.testfile, regex, sign)
        comment_multi_single = readMultiLineSame(self.testfile, self.syntax_single)
        comment_multi_double = readMultiLineSame(self.testfile, self.syntax_double)
        comment_contSingleline = contSingleLines(comment_single)
        file = self.testfile.split("/")
        output = {
        "metadata": {
        "filename": file[-1],
        "lang": "Python",
        "total_lines": comment_single[1],
        "total_lines_of_comments": comment_single[3] + comment_multi_single[3] + comment_multi_double[3],
        "blank_lines": comment_single[2],
        "sloc": comment_single[1] - (comment_single[3] + comment_multi_single[3] + comment_multi_double[3] + comment_single[2])
        },
        "single_line_comment": [],
        "cont_single_line_comment": [],
        "multi_line_comment": []
        }

        if comment_contSingleline:
            comment_single = comment_contSingleline[0]

        if comment_single:
            for i in comment_single[0]:
                output['single_line_comment'].append({"line_number":i[0], "comment": i[1]})

        if comment_contSingleline:
            for idx, i in enumerate(comment_contSingleline[1]):
                output['cont_single_line_comment'].append({"start_line": comment_contSingleline[1][idx], "end_line": comment_contSingleline[2][idx], "comment": comment_contSingleline[3][idx]})

        if comment_multi_single:
            try:
                for idx, i in enumerate(comment_multi_single[0]):
                    output['multi_line_comment'].append({"start_line": comment_multi_single[0][idx], "end_line": comment_multi_single[1][idx], "comment": comment_multi_single[2][idx]})
            except:
                pass

        if comment_multi_double:
            try:
                for idx, i in enumerate(comment_multi_double[0]):
                    output['multi_line_comment'].append({"start_line": comment_multi_double[0][idx], "end_line": comment_multi_double[1][idx], "comment": comment_multi_double[2][idx]})
            except:
                pass

        self.assertEqual(output, expected)

    def test_Source(self):
        name = "source.txt"
        newfile = python.pythonSource(self.testfile, name)

        self.assertTrue(newfile)
