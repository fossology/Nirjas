#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import extractor

def readSingleLine(file, regex):
    with open(file) as f:
        for lineNumber, line in enumerate(f, start=1):
            if f.readline() == regex: #regex for "#"
                content = re.findall(regex, line)
                return lineNumber, content
                

def readMultiLineSame(file, syntax: str):
    lines, content = [],[]
    closingCount = 0
    copy = False
    with open("file") as f:
        for lineNumber, line in enumerate(f, start=1):
            if line.strip() == syntax:
                closingCount+=1
                copy = True
                if closingCount%2 == 0 and closingCount!=0:
                    copy = False
                lines.append(lineNumber)
            if copy:
                content.append(line)
    return lines, content

def readMultiLineDiff(file, startSyntax: str, endSyntax: str):
    lines, content = [], []
    copy = False
    with open("file") as f:
        for lineNumber, line in enumerate(f, start=1):
            if line.strip() == startSyntax:
                copy = True
                lines.append(lineNumber)
            elif line.strip() == endSyntax:
                copy = False
                lines.append(lineNumber)
            if copy:
                content.append(line)
    return lines, content


class CommentSyntax:
    
    def __init__(self):
        pass

    def hash(self,file):
        '''
        sign: #
        '''
        self.pattern_hash = r'''(#+\s*[\w #\.()@+-_*\d]*)'''
        # comment = re.findall(pattern_single, file)
        return readSingleLine(file, self.pattern_hash)

    def percentage(self,file):
        '''
        sign: %
        '''
        self.pattern_percentage = r'''(\%\s*[\w #\.()@+-_*\d]*)'''
        # comment = re.findall(pattern_percentage,file)
        return readSingleLine(file, self.pattern_percentage)

    def doubleSlash(self,file):
        '''
        sign: //
        '''
        self.pattern_doubleSlash = r'''(\/\/\s*[\w #\.()@+-_*\d]*)'''
        # comment = re.findall(pattern_doubleSlash, file)
        return readSingleLine(file, self.pattern_doubleSlash)

    def singleQuotes(self,file):
        '''
        sign: '''  '''
        '''
        self.syntax = "'''"
        # pattern_multiline = r'\'\'\'(.*?)\'\'\''  #re.DOTALL flag will be used
        # comment = re.findall(pattern_multiline,file, re.DOTALL)
        return readMultiLineSame(file, self.syntax)

    def doubleQuotes(self,file):
        '''
        sign: """ """
        '''
        self.syntax = '"""'
        # pattern_doubleQuotes = r'\"\"\"(.*?)\"\"\"' #re.DOTALL flag will be used
        # comment = re.findall(pattern_doubleQuotes,file,re.DOTALL)
        return readMultiLineSame(file, self.syntax)

    def doubleDash(self,file):
        '''
        sign: --
        '''
        self.pattern_doubleDash = r'''(\-\-\s*[\w #\.()@+-_*\d]*)'''
        # comment = re.findall(pattern_doubleDash,file)
        return readSingleLine(file, self.pattern_doubleDash)

    def slashStar(self,file):
        '''
        sign: /* ~ */
        '''
        self.start = "/*"
        self.end = "*/"
        # pattern_slashStar = r'/\*(.*?)\*/'
        # comment = re.findall(pattern_slashStar,file, re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end)

    def gtExclamationDash(self,file):
        '''
        sign : <!-- ~ -->
        '''
        self.start = "<!--"
        self.end = "-->"
        # pattern_exclamationDash = r'\<\!(.*?)\>'
        # comment = re.findall(pattern_exclamationDash, file, re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end)

    def beginCut(self,file):
        '''
        sign: =begin ~ =cut
        '''
        self.start = "=begin"
        self.end = "=cut"
        # pattern_beginCut = r'\=begin(.*?)\=cut'
        # comment = re.findall(pattern_beginCut,file, re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end)

    def beginEnd(self,file):
        '''
        sign: =begin ~ =end
        '''
        self.start = "=begin"
        self.end = "=end"
        # pattern_beginEnd = r'\=begin(.*?)\=end'
        # comment = re.findall(pattern_beginEnd,file,re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end)

    def curlybracesDash(self,file):
        '''
        sign: {- ~ -}
        '''
        self.start = "{-"
        self.end = "-}"
        # pattern_curlybracesDash = r'\{\-(.*?)\-\}'
        # comment = re.findall(pattern_curlybracesDash,file,re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end)

    def percentageCurlybraces(self,file):
        '''
        sign: %{ ~ %}
        '''
        self.start = "%{"
        self.end = "%}"
        # pattern_percentageCurlybraces = r'\%\{(.*?)\%\}'
        # comment = re.findall(pattern_percentageCurlybraces,file,re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end)
