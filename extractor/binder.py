#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2020  Ayush Bhardwaj (classicayush@gmail.com), Kaushlendra Pratap (kaushlendrapratap.9837@gmail.com)

SPDX-License-Identifier: LGPL-2.1

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''

import re


def readSingleLine(file, regex):
    content = []
    with open(file) as f:
        for lineNumber, line in enumerate(f, start=1):
            output = re.findall(regex, line)
            output = ''.join(output)
            if output:
                content.append([lineNumber, output[1:]])
    return content
                

def readMultiLineSame(file, syntax: str):
    lines, output = [], []
    content = ""
    closingCount = 0
    copy = False
    with open(file) as f:
        for lineNumber, line in enumerate(f, start=1):
            if line.strip() == syntax:
                closingCount+=1
                copy = True
                if closingCount%2 == 0 and closingCount!=0:
                    copy = False
                lines.append(lineNumber)
            if copy:
                # content = content + line.rstrip()
                output.append(line.rstrip())
            for i in output:
                if i == "'''" or i == "":
                    output.remove(i)
    return [lines, output]

def readMultiLineDiff(file, startSyntax: str, endSyntax: str):
    lines, content = [], []
    copy = False
    with open(file) as f:
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
        self.pattern_hash = r'''(#+\s*[\!\w #\.()@+-_*\d]*)'''
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

    def tripleSlash(self,file):
        '''
        sign: ///
        '''
        self.pattern_tripleSlash = r'''(\/\/\/\s*[\w #\.()@+-_*\d]*)'''
        # comment = re.findall(pattern_doubleSlash, file)
        return readSingleLine(file, self.pattern_tripleSlash)
    
    def slashDoubleStar(self,file):
        '''
        sign: /** ~ */
        '''
        self.start = "/**"
        self.end = "*/"
        # pattern_slashStar = r'/\*(.*?)\*/'
        # comment = re.findall(pattern_slashStar,file, re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end)