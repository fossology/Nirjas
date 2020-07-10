import unittest
import re, os
from languages import shell
from binder import readSingleLine,readMultiLineDiff

class ShellTest(unittest.TestCase):
    
    def test_output(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.sh")
        regex = r'''(#+\s*[\!\w #\.()@+-_*\d]*)'''
        comment_single = shell.readSingleLine(path,regex)
        self.assertTrue(comment_single)



    def test_outputFormat(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.sh")
        regex = r'''(#+\s*[\!\w #\.()@+-_*\d]*)'''
        expected = shell.shellExtractor(path)
        comment_single = readSingleLine(path,regex)
        file = path.split("/")
        output = {
        "metadata": [{
        "filename": file[-1],
        "lang": "Shell",
        "total_lines": comment_single[1],
        "total_lines_of_comments": comment_single[3],
        "blank_lines": comment_single[2],
        "sloc": comment_single[1]-(comment_single[3]+comment_single[2])
        }],
        "single_line_comment": [],
        "multi_line_comment": []
        }
        if comment_single:
            for i in comment_single[0]:
                output['single_line_comment'].append({"line_number" :i[0],"comment": i[1]})
        self.assertEqual(output,expected)

    def test_Source(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.sh")
        name = "source.txt"
        newfile = shell.shellSource(path,name)

        self.assertTrue(newfile)  