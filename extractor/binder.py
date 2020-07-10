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
    total_lines, line_of_comments, blank_lines = 0,0,0
    with open(file) as f:
        for lineNumber, line in enumerate(f, start=1):
            total_lines += 1
            output = re.findall(regex, line)
            output = ''.join(output)

            if output:
                output = output[1:]
                content.append([lineNumber, output.strip()])

            line = line.replace(" ","")

            if line:
                if line[0] == '#':
                    line_of_comments += 1

            if not line.strip():
                blank_lines += 1

    return content, total_lines, blank_lines, line_of_comments
                

def readMultiLineSame(file, syntax: str):
    lines, output, startLine, endLine = [], [], [], []
    content = ""
    closingCount, lines_of_comment = 0,0
    copy = False
    with open(file) as f:
        for lineNumber, line in enumerate(f, start=1):
            if line.strip() == syntax:
                closingCount+=1
                copy = True
                if closingCount%2 == 0 and closingCount!=0:
                    copy = False
                    output.append(content)
                    content = ""
                    endLine.append(lineNumber)
                lines.append(lineNumber)

            if copy:
                lines_of_comment += 1
                content = content + line.replace('\n', '')

            output = [s.strip("'''") for s in output]
        
        result = [lines, output]
        startLine = list(filter(lambda x: x not in endLine, lines))
    return startLine, endLine, output, lines_of_comment


def readMultiLineDiff(file, startSyntax: str, endSyntax: str):
    output, startLine, endLine = [], [], []
    content = ""
    total_lines, line_of_comments, blank_lines = 0,0,0
    copy = False
    with open(file) as f:
        for lineNumber, line in enumerate(f, start=1):
            total_lines += 1
            if line.strip() == startSyntax:
                copy = True
                startLine.append(lineNumber)
            elif line.strip() == endSyntax:
                copy = False
                output.append(content)
                content = ""
                endLine.append(lineNumber)
            if copy:
                line_of_comments += 1
                content = content + line.replace('\n','')
            if not line.strip():
                blank_lines += 1
        line_of_comments += len(output)
        output = [s.strip(startSyntax) for s in output]
        output = [s.strip(endSyntax) for s in output]
    return startLine, endLine, output, line_of_comments, total_lines, blank_lines


class CommentSyntax:
    
    def __init__(self):
        pass

    def hash(self,file):
        '''
        sign: #
        '''
        self.pattern_hash = r'''(#+\s*[\!\w #\.()@+-_*\d]*)'''
        return readSingleLine(file, self.pattern_hash)

    def percentage(self,file):
        '''
        sign: %
        '''
        self.pattern_percentage = r'''(\%\s*[\w #\.()@+-_*\d]*)'''
        return readSingleLine(file, self.pattern_percentage)

    def doubleSlash(self,file):
        '''
        sign: //
        '''
        self.pattern_doubleSlash = r'''(\/\/\s*[\w #\.()@+-_*\d]*)'''
        return readSingleLine(file, self.pattern_doubleSlash)

    def singleQuotes(self,file):
        '''
        sign: '''  '''
        '''
        self.syntax = "'''"
        return readMultiLineSame(file, self.syntax)

    def doubleQuotes(self,file):
        '''
        sign: """ """
        '''
        self.syntax = '"""'
        return readMultiLineSame(file, self.syntax)

    def doubleDash(self,file):
        '''
        sign: --
        '''
        self.pattern_doubleDash = r'''(\-\-\s*[\w #\.()@+-_*\d]*)'''
        return readSingleLine(file, self.pattern_doubleDash)

    def slashStar(self,file):
        '''
        sign: /* ~ */
        '''
        self.start = "/*"
        self.end = "*/"
        return readMultiLineDiff(file, self.start, self.end)

    def gtExclamationDash(self,file):
        '''
        sign : <!-- ~ -->
        '''
        self.start = "<!--"
        self.end = "-->"
        return readMultiLineDiff(file, self.start, self.end)

    def beginCut(self,file):
        '''
        sign: =begin ~ =cut
        '''
        self.start = "=begin"
        self.end = "=cut"
        return readMultiLineDiff(file, self.start, self.end)

    def beginEnd(self,file):
        '''
        sign: =begin ~ =end
        '''
        self.start = "=begin"
        self.end = "=end"
        return readMultiLineDiff(file, self.start, self.end)

    def curlybracesDash(self,file):
        '''
        sign: {- ~ -}
        '''
        self.start = "{-"
        self.end = "-}"
        return readMultiLineDiff(file, self.start, self.end)

    def percentageCurlybraces(self,file):
        '''
        sign: %{ ~ %}
        '''
        self.start = "%{"
        self.end = "%}"
        return readMultiLineDiff(file, self.start, self.end)

    def tripleSlash(self,file):
        '''
        sign: ///
        '''
        self.pattern_tripleSlash = r'''(\/\/\/\s*[\w #\.()@+-_*\d]*)'''
        return readSingleLine(file, self.pattern_tripleSlash)
    
    def slashDoubleStar(self,file):
        '''
        sign: /** ~ */
        '''
        self.start = "/**"
        self.end = "*/"
        return readMultiLineDiff(file, self.start, self.end)