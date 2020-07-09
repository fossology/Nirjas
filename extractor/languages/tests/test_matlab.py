import unittest
import re, os
from languages import matlab
from binder import readSingleLine,readMultiLineDiff

class matlabTest(unittest.TestCase):
    
    def test_output(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.m")
        regex = r'''(\%\s*[\w #\.()@+-_*\d]*)'''
        self.syntax_start = "%{"
        self.syntax_end = "%}"
        comment_single = matlab.readSingleLine(path,regex)
        comment_multiline = matlab.readMultiLineDiff(path,self.syntax_start,self.syntax_end)

        self.assertTrue(comment_single)
        self.assertTrue(comment_multiline)



    def test_outputFormat(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.m")
        regex = r'''(\%\s*[\w #\.()@+-_*\d]*)'''
        self.syntax_start = "%{"
        self.syntax_end = "%}"
        expected = matlab.matlabExtractor(path)
        comment_single = readSingleLine(path,regex)
        comment_multiline = readMultiLineDiff(path,self.syntax_start,self.syntax_end)
        print(type(comment_single[3]),type(comment_multiline[3]))
        file = path.split("/")
        output = {
        "metadata": [{
        "filename": file[-1],
        "lang": "MATLAB",
        "total_lines": comment_multiline[1],
        "total_lines_of_comments": comment_multiline[3]+comment_single[3],
        "blank_lines": comment_multiline[2],
        "sloc": comment_multiline[1]-(comment_multiline[3]+comment_single[3]+comment_multiline[2])
        }],
        "single_line_comment": [],
        "multi_line_comment": []
        }
        if comment_multiline:
            for i in comment_multiline[0]:
                output['single_line_comment'].append({"line_number" :i[0],"comment": i[1]})

        if comment_single:
            for idx,i in enumerate(comment_single[0]):
                output['multi_line_comment'].append({"start_line": comment_single[0][idx], "end_line": comment_single[1][idx], "comment": comment_single[2][idx]})

        self.assertEqual(output,expected)  