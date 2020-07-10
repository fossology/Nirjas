import unittest
import re, os
from languages import css
from binder import readSingleLine,readMultiLineDiff

class CssTest(unittest.TestCase):
    
    def test_output(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.css")
        self.syntax_start = "/*"
        self.syntax_end ='*/'
        comment_multiline = css.readMultiLineDiff(path,self.syntax_start,self.syntax_end)

        self.assertTrue(comment_multiline)



    def test_outputFormat(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.m")
        self.syntax_start = "/*"
        self.syntax_end ='*/'
        expected = css.cssExtractor(path)
        comment_multiline = readMultiLineDiff(path,self.syntax_start,self.syntax_end)
        file = path.split("/")
        output = {
        "metadata": [{
        "filename": file[-1],
        "lang": "CSS",
        "total_lines": comment_multiline[4],
        "total_lines_of_comments": comment_multiline[3],
        "blank_lines": comment_multiline[5],
        "sloc": comment_multiline[4]-(comment_multiline[3]+comment_multiline[5])
        }],
        "single_line_comment": [],
        "multi_line_comment": []
        }
        if comment_multiline:
            for idx,i in enumerate(comment_multiline[0]):
                output['multi_line_comment'].append({"start_line": comment_multiline[0][idx], "end_line": comment_multiline[1][idx], "comment": comment_multiline[2][idx]})

        self.assertEqual(output,expected)  
    
    def test_Source(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.css")
        name = "source.txt"
        newfile = css.cssSource(path,name)

        self.assertTrue(newfile)