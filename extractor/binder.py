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

    def percentage(self,file):
        '''
        sign: %
        '''
        pattern_percentage = r'''(\%\s*[\w #\.()@+-_*\d]*)'''
        comment = re.findall(pattern_percentage,file)
        return comment

    def doubleSlash(self,file):
        '''
        sign: //
        '''
        pattern_doubleSlash = r'''(\/\/\s*[\w #\.()@+-_*\d]*)'''
        comment = re.findall(pattern_doubleSlash, file)
        return comment

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

    def doubleDash(self,file):
        '''
        sign: --
        '''
        pattern_doubleDash = r'''(\-\-\s*[\w #\.()@+-_*\d]*)'''
        comment = re.findall(pattern_doubleDash,file)
        return comment

    def slashStar(self,file):
        '''
        sign: /* ~ */
        '''
        pattern_slashStar = r'/\*(.*?)\*/'
        comment = re.findall(pattern_slashStar,file, re.DOTALL)
        return comment

    def gtExclamationDash(self,file):
        '''
        sign : <!-- ~ -->
        '''
        pattern_exclamationDash = r'\<\!(.*?)\>'
        comment = re.findall(pattern_exclamationDash, file, re.DOTALL)
        return comment

    def beginCut(self,file):
        '''
        sign: =begin ~ =cut
        '''
        pattern_beginCut = r'\=begin(.*?)\=cut'
        comment = re.findall(pattern_beginCut,file, re.DOTALL)
        return comment

    def beginEnd(self,file):
        '''
        sign: =begin ~ =end
        '''
        pattern_beginEnd = r'\=begin(.*?)\=end'
        comment = re.findall(pattern_beginEnd,file,re.DOTALL)
        return comment

    def curlybracesDash(self,file):
        '''
        sign: {- ~ -}
        '''
        pattern_curlybracesDash = r'\{\-(.*?)\-\}'
        comment = re.findall(pattern_curlybracesDash,file,re.DOTALL)
        return comment

    def percentageCurlybraces(self,file):
        '''
        sign: %{ ~ %}
        '''
        pattern_percentageCurlybraces = r'\%\{(.*?)\%\}'
        comment = re.findall(pattern_percentageCurlybraces,file,re.DOTALL)
        return comment
