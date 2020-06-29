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


def readSingleLine(file, regex, current_path):
    content = []
    total_lines, line_of_comments, blank_lines = 0,0,0
    with open(current_path) as f:
        for lineNumber, line in enumerate(f, start=1):
            total_lines += 1
            output = re.findall(regex, line)
            output = ''.join(output)

            if output:
                content.append([lineNumber, output[1:]])

            line = line.replace(" ","")

            if line:
                if line[0] == "#":
                    line_of_comments += 1

            if not line.strip():
                blank_lines += 1

    return content, total_lines, blank_lines, line_of_comments
                

def readMultiLineSame(file, syntax: str, current_path):
    lines, output, startLine, endLine = [], [], [], []
    content = ""
    closingCount, lines_of_comment = 0,0
    copy = False
    with open(current_path) as f:
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
                content = content + line.replace('\n', ' ')

            output = [s.strip("'''") for s in output]
        
        result = [lines, output]
        startLine = list(filter(lambda x: x not in endLine, lines))
    return startLine, endLine, output, lines_of_comment


def readMultiLineDiff(file, startSyntax: str, endSyntax: str, current_path):
    output, startLine, endLine = [], [], []
    content = ""
    lines_of_comment = 0
    copy = False
    with open(file) as f:
        for lineNumber, line in enumerate(f, start=1):
            if line.strip() == startSyntax:
                copy = True
                startLine.append(lineNumber)
            elif line.strip() == endSyntax:
                copy = False
                output.append(content)
                content = ""
                endLine.append(lineNumber)
            if copy:
                lines_of_comment += 1
                content = content + line.replace('\n',' ')
        lines_of_comment += len(output)
        output = [s.strip(startSyntax) for s in output]
        output = [s.strip(endSyntax) for s in output]
    return startLine, endLine, output, lines_of_comment


class CommentSyntax:
    
    def __init__(self):
        pass

    def hash(self,file,current_path):
        '''
        sign: #
        '''
        self.pattern_hash = r'''(#+\s*[\!\w #\.()@+-_*\d]*)'''
        # comment = re.findall(pattern_single, file)
        return readSingleLine(file, self.pattern_hash, current_path)

    def percentage(self,file,current_path):
        '''
        sign: %
        '''
        self.pattern_percentage = r'''(\%\s*[\w #\.()@+-_*\d]*)'''
        # comment = re.findall(pattern_percentage,file)
        return readSingleLine(file, self.pattern_percentage,current_path)

    def doubleSlash(self,file,current_path):
        '''
        sign: //
        '''
        self.pattern_doubleSlash = r'''(\/\/\s*[\w #\.()@+-_*\d]*)'''
        # comment = re.findall(pattern_doubleSlash, file)
        return readSingleLine(file, self.pattern_doubleSlash,current_path)

    def singleQuotes(self,file,current_path):
        '''
        sign: '''  '''
        '''
        self.syntax = "'''"
        # pattern_multiline = r'\'\'\'(.*?)\'\'\''  #re.DOTALL flag will be used
        # comment = re.findall(pattern_multiline,file, re.DOTALL)
        return readMultiLineSame(file, self.syntax,current_path)

    def doubleQuotes(self,file,current_path):
        '''
        sign: """ """
        '''
        self.syntax = '"""'
        # pattern_doubleQuotes = r'\"\"\"(.*?)\"\"\"' #re.DOTALL flag will be used
        # comment = re.findall(pattern_doubleQuotes,file,re.DOTALL)
        return readMultiLineSame(file, self.syntax,current_path)

    def doubleDash(self,file,current_path):
        '''
        sign: --
        '''
        self.pattern_doubleDash = r'''(\-\-\s*[\w #\.()@+-_*\d]*)'''
        # comment = re.findall(pattern_doubleDash,file)
        return readSingleLine(file, self.pattern_doubleDash,current_path)

    def slashStar(self,file,current_path):
        '''
        sign: /* ~ */
        '''
        self.start = "/*"
        self.end = "*/"
        # pattern_slashStar = r'/\*(.*?)\*/'
        # comment = re.findall(pattern_slashStar,file, re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end,current_path)

    def gtExclamationDash(self,file,current_path):
        '''
        sign : <!-- ~ -->
        '''
        self.start = "<!--"
        self.end = "-->"
        # pattern_exclamationDash = r'\<\!(.*?)\>'
        # comment = re.findall(pattern_exclamationDash, file, re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end,current_path)

    def beginCut(self,file,current_path):
        '''
        sign: =begin ~ =cut
        '''
        self.start = "=begin"
        self.end = "=cut"
        # pattern_beginCut = r'\=begin(.*?)\=cut'
        # comment = re.findall(pattern_beginCut,file, re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end,current_path)

    def beginEnd(self,file,current_path):
        '''
        sign: =begin ~ =end
        '''
        self.start = "=begin"
        self.end = "=end"
        # pattern_beginEnd = r'\=begin(.*?)\=end'
        # comment = re.findall(pattern_beginEnd,file,re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end,current_path)

    def curlybracesDash(self,file,current_path):
        '''
        sign: {- ~ -}
        '''
        self.start = "{-"
        self.end = "-}"
        # pattern_curlybracesDash = r'\{\-(.*?)\-\}'
        # comment = re.findall(pattern_curlybracesDash,file,re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end,current_path)

    def percentageCurlybraces(self,file,current_path):
        '''
        sign: %{ ~ %}
        '''
        self.start = "%{"
        self.end = "%}"
        # pattern_percentageCurlybraces = r'\%\{(.*?)\%\}'
        # comment = re.findall(pattern_percentageCurlybraces,file,re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end,current_path)

    def tripleSlash(self,file,current_path):
        '''
        sign: ///
        '''
        self.pattern_tripleSlash = r'''(\/\/\/\s*[\w #\.()@+-_*\d]*)'''
        # comment = re.findall(pattern_doubleSlash, file)
        return readSingleLine(file, self.pattern_tripleSlash,current_path)
    
    def slashDoubleStar(self,file,current_path):
        '''
        sign: /** ~ */
        '''
        self.start = "/**"
        self.end = "*/"
        # pattern_slashStar = r'/\*(.*?)\*/'
        # comment = re.findall(pattern_slashStar,file, re.DOTALL)
        return readMultiLineDiff(file, self.start, self.end,current_path)