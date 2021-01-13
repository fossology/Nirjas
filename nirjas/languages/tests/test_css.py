import unittest
import os
from nirjas.languages import css
from nirjas.binder import readMultiLineDiff


class CssTest(unittest.TestCase):
    testfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), "TestFiles/textcomment.css")

    def test_output(self):
        self.syntax_start = "/*"
        self.syntax_end = '*/'
        comment_multiline = css.readMultiLineDiff(self.testfile, self.syntax_start, self.syntax_end)

        self.assertTrue(comment_multiline)

    def test_outputFormat(self):
        self.syntax_start = "/*"
        self.syntax_end = '*/'
        expected = css.cssExtractor(self.testfile).get_dict()
        comment_multiline = readMultiLineDiff(self.testfile, self.syntax_start, self.syntax_end)
        file = self.testfile.split("/")
        output = {
        "metadata": {
        "filename": file[-1],
        "lang": "CSS",
        "total_lines": comment_multiline[4],
        "total_lines_of_comments": comment_multiline[3],
        "blank_lines": comment_multiline[5],
        "sloc": comment_multiline[4] - (comment_multiline[3] + comment_multiline[5])
        },
        "single_line_comment": [],
        "cont_single_line_comment": [],
        "multi_line_comment": []
        }
        if comment_multiline:
            try:
                for idx, i in enumerate(comment_multiline[0]):
                    output['multi_line_comment'].append({"start_line": comment_multiline[0][idx], "end_line": comment_multiline[1][idx], "comment": comment_multiline[2][idx]})
            except:
                pass

        self.assertEqual(output, expected)

    def test_Source(self):
        name = "source.txt"
        newfile = css.cssSource(self.testfile, name)

        self.assertTrue(newfile)
