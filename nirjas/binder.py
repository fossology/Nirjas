#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (C) 2020  Ayush Bhardwaj (classicayush@gmail.com),
Kaushlendra Pratap (kaushlendrapratap.9837@gmail.com)

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
"""

import re


def readSingleLine(file, regex):
    """
    Read file line by line and match the given regex to get comment.
    Return comments, lines read, blank lines, and lines with comments.
    Each comment entry is [line_number, comment, is_full_line] where
    is_full_line tells whether the comment occupies the whole line or
    trails code on the same line.
    """
    content = []
    total_lines, line_of_comments, blank_lines = 0, 0, 0
    with open(file, encoding="utf-8", errors="replace") as f:
        for line_number, line in enumerate(f, start=1):
            total_lines += 1
            match = re.search(regex, line, re.I)
            if match:
                line_of_comments += 1
                output = "".join(match.groups())
                if output:
                    is_full_line = line[: match.start()].strip() == ""
                    content.append([line_number, output.strip(), is_full_line])

            line = line.strip()

            if line == "":
                blank_lines += 1

    return content, total_lines, blank_lines, line_of_comments


def contSingleLines(data):
    """
    Merge consecutive single line comments as cont_single_line_comment.
    Only comments that occupy their whole line are merged; a comment
    that trails code on the same line is an independent comment, so it
    is never part of a continuation block.
    """
    start_line, end_line, output = [], [], []
    remaining, streak = [], []

    def flushStreak():
        if len(streak) > 1:
            start_line.append(streak[0][0])
            end_line.append(streak[-1][0])
            output.append("".join(" " + entry[1] for entry in streak))
        else:
            remaining.extend(streak)
        streak.clear()

    for entry in data[0]:
        # Entries without the flag come from older callers; treat them
        # as full-line comments to keep the previous behaviour.
        is_full_line = entry[2] if len(entry) > 2 else True
        if not is_full_line:
            flushStreak()
            remaining.append(entry)
            continue
        if streak and entry[0] != streak[-1][0] + 1:
            flushStreak()
        streak.append(entry)
    flushStreak()

    data = ([entry[:2] for entry in remaining], *data[1:])
    return data, start_line, end_line, output


def readMultiLineSame(file, syntax: str):
    """
    Read multiline comments where starting and ending symbols are same.
    """
    start_line, end_line, output = [], [], []
    content = ""
    if '"' in syntax:
        syntax_in_string = "'" + syntax
    elif "'" in syntax:
        syntax_in_string = '"' + syntax
    closingCount, lines_of_comment = 0, 0
    copy = False
    with open(file, encoding="utf-8", errors="replace") as f:
        for line_number, line in enumerate(f, start=1):
            if syntax in line and syntax_in_string not in line:
                closingCount += 1
                copy = True
                if line.count(syntax) == 2:
                    # Start and end on same line
                    closingCount = 2
                    content = line.replace("\n", " ")
                    start_line.append(line_number)
                if closingCount % 2 == 0 and closingCount != 0:
                    copy = False
                    output.append(content.strip())
                    content = ""
                    end_line.append(line_number)
                else:
                    start_line.append(line_number)

            if copy:
                lines_of_comment += 1
                content = content + line.replace("\n", " ")

    output = [s.strip(syntax).strip() for s in output]
    return start_line, end_line, output, lines_of_comment


def readMultiLineDiff(file, startSyntax: str, endSyntax: str):
    """
    Read multiline comments where starting and ending symbols are different.
    """
    output, startLine, endLine = [], [], []
    content = ""
    total_lines, line_of_comments, blank_lines = 0, 0, 0
    inComment = False
    with open(file, encoding="utf-8", errors="replace") as f:
        for lineNumber, line in enumerate(f, start=1):
            total_lines += 1
            stripped_line = line.strip()
            if startSyntax in stripped_line and not inComment:
                inComment = True
                startLine.append(lineNumber)
                line = line[line.find(startSyntax) + len(startSyntax):]
            if endSyntax in stripped_line and inComment:
                inComment = False
                line = line[: line.rfind(endSyntax) + len(endSyntax)]
                content = content + line.replace("\n", " ")
                content = content.strip(startSyntax).strip(endSyntax).strip()
                output.append(content)
                content = ""
                endLine.append(lineNumber)
                continue
            if inComment:
                content = content + (line.replace("\n", " ")).strip()
            if stripped_line == "":
                blank_lines += 1
        min_length = min(len(startLine), len(endLine))
        for idx in range(min_length):
            line_of_comments = line_of_comments + (endLine[idx] - startLine[idx]) + 1
        line_of_comments += len(output)
        output = [s.strip(startSyntax).strip(endSyntax).strip() for s in output]
    return (
        startLine,
        endLine,
        output,
        line_of_comments,
        total_lines,
        blank_lines,
    )  # noqa


def extractAssignedString(file):
    """
    Read file line by line and match string type variable to get string.
    Return the content of the string.
    """
    content = []
    regex = r"=\s*['\"](.+?)['\"]"
    total_lines, line_of_assignedString = 0, 0
    with open(file, encoding="utf-8", errors="replace") as f:
        for line_number, line in enumerate(f, start=1):
            total_lines += 1
            output = re.findall(regex, line, re.S)
            if len(output) >= 2:
                line_of_assignedString += 1
            output = "".join(output)
            if output and len(output) > 1:
                content.append([line_number, output.strip()])
            line = line.strip()
    return content, line_of_assignedString


class CommentSyntax:
    """
    Class to hold various regex and helper functions based on comment format
    used by a language.
    """

    def __init__(self):
        self.sign = None
        self.pattern = None
        self.start = None
        self.end = None

    def hash(self, file):
        """
        sign: #
        """
        self.sign = "#"
        self.pattern = r"""(?<!["'`])#+\s*(.*)"""
        return readSingleLine(file, self.pattern)

    def hashNoCurl(self, file):
        """
        sign: #
        """
        self.sign = "#"
        self.pattern = r"""(?<!["'`])#+(?!\{)\s*(.*)"""
        return readSingleLine(file, self.pattern)

    def percentage(self, file):
        """
        sign: %
        """
        self.sign = "%"
        self.pattern = r"""(?<!["'`])\%\s*(.*)"""
        return readSingleLine(file, self.pattern)

    def doubleSlash(self, file):
        """
        sign: //
        """
        self.sign = "//"
        self.pattern = r"""(?<![pst'"`]:)\/\/\s*(.*)"""
        return readSingleLine(file, self.pattern)

    def doubleNotTripleSlash(self, file):
        """
        sign: //
        """
        self.sign = "//"
        self.pattern = r"""(?<!\/)\/\/(?!\/)\s*(.*)"""
        return readSingleLine(file, self.pattern)

    def singleQuotes(self, file):
        """
        sign: '''  '''
        """
        self.sign = "'''"
        return readMultiLineSame(file, self.sign)

    def doubleQuotes(self, file):
        '''
        sign: """ """
        '''
        self.sign = '"""'
        return readMultiLineSame(file, self.sign)

    def doubleDash(self, file):
        """
        sign: --
        """
        self.sign = "--"
        self.pattern = r"""(?<!["'`])\-\-\s*(.*)"""
        return readSingleLine(file, self.pattern)

    def slashStar(self, file):
        """
        sign: /* ~ */
        """
        self.start = "/*"
        self.end = "*/"
        return readMultiLineDiff(file, self.start, self.end)

    def gtExclamationDash(self, file):
        """
        sign : <!-- ~ -->
        """
        self.start = "<!--"
        self.end = "-->"
        return readMultiLineDiff(file, self.start, self.end)

    def beginCut(self, file):
        """
        sign: =begin ~ =cut
        """
        self.start = "=begin"
        self.end = "=cut"
        return readMultiLineDiff(file, self.start, self.end)

    def beginEnd(self, file):
        """
        sign: =begin ~ =end
        """
        self.start = "=begin"
        self.end = "=end"
        return readMultiLineDiff(file, self.start, self.end)

    def curlybracesDash(self, file):
        """
        sign: {- ~ -}
        """
        self.start = "{-"
        self.end = "-}"
        return readMultiLineDiff(file, self.start, self.end)

    def percentageCurlybraces(self, file):
        """
        sign: %{ ~ %}
        """
        self.start = "%{"
        self.end = "%}"
        return readMultiLineDiff(file, self.start, self.end)

    def tripleSlash(self, file):
        """
        sign: ///
        """
        self.sign = "///"
        self.pattern = r"""(?<!["'`])\/\/\/\s*(.*)"""
        return readSingleLine(file, self.pattern)

    def slashDoubleStar(self, file):
        """
        sign: /** ~ */
        """
        self.start = "/**"
        self.end = "*/"
        return readMultiLineDiff(file, self.start, self.end)

    def hashEqual(self, file):
        """
        sign: #= ~ =#
        """
        self.start = "#="
        self.end = "=#"
        return readMultiLineDiff(file, self.start, self.end)
