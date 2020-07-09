import unittest
import re, os
from languages import r
from binder import readSingleLine,readMultiLineDiff

class rTest(unittest.TestCase):
    
    def test_output(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.R")
        regex = r'''(#+\s*[\!\w #\.()@+-_*\d]*)'''
        comment_single = r.readSingleLine(path,regex)
        self.assertTrue(comment_single)



    def test_outputFormat(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.R")
        regex = r'''(#+\s*[\!\w #\.()@+-_*\d]*)'''
        expected = r.rExtractor(path)
        comment_single = readSingleLine(path,regex)
        file = path.split("/")
        output = {
        "metadata": [{
        "filename": file[-1],
        "lang": "R",
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
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.R")
        name = "source.txt"
        newfile = r.rSource(path,name)

        self.assertTrue(newfile)  