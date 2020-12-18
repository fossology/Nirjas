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
from itertools import groupby
from operator import itemgetter


def readSingleLine(file, regex, sign):
    '''
    Read file line by line and match the given regex to get comment.
    Return comments, lines read, blank lines, and lines with comments.
    '''
    content = []
    total_lines, line_of_comments, blank_lines = 0, 0, 0
    with open(file) as f:
        for line_number, line in enumerate(f, start=1):
            total_lines += 1
            output = re.findall(regex, line, re.I)
            if len(output) > 0:
                line_of_comments += 1
            output = ''.join(output)

            if output:
                content.append([line_number, output.strip()])

            line = line.strip()

            if line == '':
                blank_lines += 1

    return content, total_lines, blank_lines, line_of_comments


def contSingleLines(data):
    '''
    Merge consecutive single line comments as cont_single_line_comment
    '''
    lines, start_line, end_line, output = [], [], [], []
    content = ""
    for i in data[0]:
        lines.append(i[0])

    for a, b in groupby(enumerate(lines), lambda x: x[0] - x[1]):
        temp = list(map(itemgetter(1), b))
        content = ""

        if len(temp) > 1:
            start_line.append(temp[0])
            end_line.append(temp[-1])
            for i in temp:
                comment = [x[1] for x in data[0] if x[0] == i]
                [data[0].remove(x) for x in data[0] if x[0] == i]
                content = content + ' ' + comment[0]
            output.append(content)
    return data, start_line, end_line, output


def readMultiLineSame(file, syntax: str):
    '''
    Read multiline comments where starting and ending symbols are same.
    '''
    lines, output, start_line, end_line = [], [], [], []
    content = ""
    closingCount, lines_of_comment = 0, 0
    copy = False
    with open(file) as f:
        for line_number, line in enumerate(f, start=1):
            if syntax in line:
                closingCount += 1
                copy = True
                if closingCount % 2 == 0 and closingCount != 0:
                    copy = False
                    output.append(content.strip())
                    content = ""
                    end_line.append(line_number)
                lines.append(line_number)

            if copy:
                lines_of_comment += 1
                content = content + line.replace('\n', ' ')

            output = [s.strip(syntax).strip() for s in output]

        start_line = list(filter(lambda x: x not in end_line, lines))
    return start_line, end_line, output, lines_of_comment


def readMultiLineDiff(file, startSyntax: str, endSyntax: str):
    '''
    Read multiline comments where starting and ending symbols are different.
    '''
    output, startLine, endLine = [], [], []
    content = ""
    total_lines, line_of_comments, blank_lines = 0, 0, 0
    copy = False
    with open(file) as f:
        for lineNumber, line in enumerate(f, start=1):
            total_lines += 1
            if startSyntax in line:
                copy = True
                startLine.append(lineNumber)
                line = line[line.find(startSyntax) + len(startSyntax):]
            if endSyntax in line:
                copy = False
                line = line[:line.rfind(endSyntax) + len(endSyntax)]
                content = content + line.replace('\n', ' ')
                content = content.strip(startSyntax).strip(endSyntax).strip()
                output.append(content)
                content = ""
                endLine.append(lineNumber)
                continue
            if copy:
                content = content + (line.replace('\n', ' ')).strip()
            if line.strip() == '':
                blank_lines += 1
        for idx, i in enumerate(endLine):
            line_of_comments = line_of_comments + (endLine[idx] - startLine[idx]) + 1
        line_of_comments += len(output)
        output = [s.strip(startSyntax).strip(endSyntax).strip() for s in output]
    return startLine, endLine, output, line_of_comments, total_lines, blank_lines


class CommentSyntax:

    def __init__(self):
        pass

    def hash(self, file):
        '''
        sign: #
        '''
        self.sign = '#'
        self.pattern_hash = r'''#+\s*(.*)'''
        return readSingleLine(file, self.pattern_hash, self.sign)

    def percentage(self, file):
        '''
        sign: %
        '''
        self.sign = '%'
        self.pattern_percentage = r'''\%\s*(.*)'''
        return readSingleLine(file, self.pattern_percentage, self.sign)

    def doubleSlash(self, file):
        '''
        sign: //
        '''
        self.sign = '//'
        self.pattern_doubleSlash = r'''(?<![pst]:)\/\/\s*(.*)'''
        return readSingleLine(file, self.pattern_doubleSlash, self.sign)

    def doubleNotTripleSlash(self, file):
        '''
        sign: //
        '''
        self.sign = '//'
        self.pattern_doubleNotTripleSlash = r'''(?<!\/)\/\/(?!\/)\s*(.*)'''
        return readSingleLine(file, self.pattern_doubleNotTripleSlash, self.sign)

    def singleQuotes(self, file):
        """
        sign: '''  '''
        """
        self.syntax = "'''"
        return readMultiLineSame(file, self.syntax)

    def doubleQuotes(self, file):
        '''
        sign: """ """
        '''
        self.syntax = '"""'
        return readMultiLineSame(file, self.syntax)

    def doubleDash(self, file):
        '''
        sign: --
        '''
        self.sign = '--'
        self.pattern_doubleDash = r'''\-\-\s*(.*)'''
        return readSingleLine(file, self.pattern_doubleDash, self.sign)

    def slashStar(self, file):
        '''
        sign: /* ~ */
        '''
        self.start = "/*"
        self.end = "*/"
        return readMultiLineDiff(file, self.start, self.end)

    def gtExclamationDash(self, file):
        '''
        sign : <!-- ~ -->
        '''
        self.start = "<!--"
        self.end = "-->"
        return readMultiLineDiff(file, self.start, self.end)

    def beginCut(self, file):
        '''
        sign: =begin ~ =cut
        '''
        self.start = "=begin"
        self.end = "=cut"
        return readMultiLineDiff(file, self.start, self.end)

    def beginEnd(self, file):
        '''
        sign: =begin ~ =end
        '''
        self.start = "=begin"
        self.end = "=end"
        return readMultiLineDiff(file, self.start, self.end)

    def curlybracesDash(self, file):
        '''
        sign: {- ~ -}
        '''
        self.start = "{-"
        self.end = "-}"
        return readMultiLineDiff(file, self.start, self.end)

    def percentageCurlybraces(self, file):
        '''
        sign: %{ ~ %}
        '''
        self.start = "%{"
        self.end = "%}"
        return readMultiLineDiff(file, self.start, self.end)

    def tripleSlash(self, file):
        '''
        sign: ///
        '''
        self.sign = '///'
        self.pattern_tripleSlash = r'''\/\/\/\s*(.*)'''
        return readSingleLine(file, self.pattern_tripleSlash, self.sign)

    def slashDoubleStar(self, file):
        '''
        sign: /** ~ */
        '''
        self.start = "/**"
        self.end = "*/"
        return readMultiLineDiff(file, self.start, self.end)
