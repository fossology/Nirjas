import unittest
from extractor.languages import python
from binder import readSingleLine, readMultiLineSame

class PythonTest(unittest.TestCase):
    def test_singleLine(self):
        path = "/home/kaushlendra/Desktop/Code-Comment-Extractor/extractor/languages/tests/textcomment.py"
        name = "textcomment.py"
        comment = python.readSingleLine(name,path)
        expected = "ABCDE"
        self.assertEqual(comment,expected)