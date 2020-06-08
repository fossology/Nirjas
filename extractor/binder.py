#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import extractor

def readSingleLine(file, regex):
    with open(file) as f:
        for lineNumber, line in enumerate(f, start=1):
            if f.readline() == " # ": #regex for "#"
                return lineNumber, line
                

def readMultiLine(file, syntax):
    lines, content = [],[]
    closingCount = 0
    with open("file") as f:
        for lineNumber, line in enumerate(f, start=1):
            if line.strip() == "syntax":
                closingCount+=1
                copy = True
                if closingCount%2 == 0 and closingCount!=0:
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
        pattern_single = r'''(#+\s*[\w #\.()@+-_*\d]*)'''
        comment = re.findall(pattern_single, file)
        return comment

    def percentage(self):
        '''
        sign: %
        '''
        pass

    def doubleSlash(self):
        '''
        sign: //
        '''
        pass

    def singleQuotes(self,file):
        '''
        sign: '''  '''
        '''
        pattern_multiline = r'\'\'\'(.*?)\'\'\''  #re.DOTALL flag will be used
        comment = re.findall(pattern_multiline,file, re.DOTALL)
        return comment

    def doubleQuotes(self,file):
        '''
        sign: """ """
        '''
        pattern_doubleQuotes = r'\"\"\"(.*?)\"\"\"' #re.DOTALL flag will be used
        comment = re.findall(pattern_doubleQuotes,file,re.DOTALL)
        return comment

    def doubleDash(self):
        '''
        sign: --
        '''
        pass

    def slashStar(self,file):
        '''
        sign: /* ~ */
        '''
        pattern_slashStar = r'/\*(.*?)\*/'
        comment = re.findall(pattern_slashStar,file, re.DOTALL)
        return comment

    def gtExclamationDash(self):
        '''
        sign : <!-- ~ -->
        '''
        pass

    def beginCut(self):
        '''
        sign: =begin ~ =cut
        '''
        pass

    def beginEnd(self):
        '''
        sign: =begin ~ =end
        '''
        pass

    def curlybracesDash(self):
        '''
        sign: {- ~ -}
        '''
        pass

    def percentageCurlybraces(self):
        '''
        sign: %{ ~ %}
        '''
        pass