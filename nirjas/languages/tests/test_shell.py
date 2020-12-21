import unittest
import os
from nirjas.languages import shell
from nirjas.binder import readSingleLine


class ShellTest(unittest.TestCase):
    testfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), "TestFiles/textcomment.sh")

    def test_output(self):
        regex = r'''#+\s*(.*)'''
        sign = '#'
        comment_single = shell.readSingleLine(self.testfile, regex, sign)
        self.assertTrue(comment_single)

    def test_outputFormat(self):
        regex = r'''#+\s*(.*)'''
        expected = shell.shellExtractor(self.testfile).get_dict()
        sign = '#'
        comment_single = readSingleLine(self.testfile, regex, sign)
        comment_contSingleline = shell.contSingleLines(comment_single)
        file = self.testfile.split("/")
        output = {
        "metadata": {
        "filename": file[-1],
        "lang": "Shell",
        "total_lines": comment_single[1],
        "total_lines_of_comments": comment_single[3],
        "blank_lines": comment_single[2],
        "sloc": comment_single[1] - (comment_single[3] + comment_single[2])
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

        self.assertEqual(output, expected)

    def test_Source(self):
        name = "source.txt"
        newfile = shell.shellSource(self.testfile, name)

        self.assertTrue(newfile)
