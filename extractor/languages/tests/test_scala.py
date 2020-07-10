import unittest
import re, os
from languages import scala
from binder import readSingleLine,readMultiLineDiff

class ScalaTest(unittest.TestCase):
    
    def test_output(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.scala")
        regex = r'''(\/\/\s*[\w #\.()@+-_*\d]*)'''
        self.syntax_start = "/*"
        self.syntax_end ='*/'
        comment_single = scala.readSingleLine(path,regex)
        comment_multiline = scala.readMultiLineDiff(path,self.syntax_start,self.syntax_end)

        self.assertTrue(comment_single)
        self.assertTrue(comment_multiline)



    def test_outputFormat(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.scala")
        regex = r'''(\/\/\s*[\w #\.()@+-_*\d]*)'''
        self.syntax_start = "/*"
        self.syntax_end ='*/'
        expected = scala.scalaExtractor(path)
        comment_single = readSingleLine(path,regex)
        comment_multiline = readMultiLineDiff(path,self.syntax_start,self.syntax_end)
        file = path.split("/")
        output = {
        "metadata": [{
        "filename": file[-1],
        "lang": "Scala",
        "total_lines": comment_single[1],
        "total_lines_of_comments": comment_single[3]+comment_multiline[3],
        "blank_lines": comment_single[2],
        "sloc": comment_single[1]-(comment_single[3]+comment_multiline[3]+comment_single[2])
        }],
        "single_line_comment": [],
        "multi_line_comment": []
    }
        if comment_single:
            for i in comment_single[0]:
                output['single_line_comment'].append({"line_number" :i[0],"comment": i[1]})

        if comment_multiline:
            for idx,i in enumerate(comment_multiline[0]):
                output['multi_line_comment'].append({"start_line": comment_multiline[0][idx], "end_line": comment_multiline[1][idx], "comment": comment_multiline[2][idx]})

        self.assertEqual(output,expected)

    def test_Source(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.scala")
        name = "source.txt"
        newfile = scala.scalaSource(path,name)

        self.assertTrue(newfile)  