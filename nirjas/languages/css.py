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

from nirjas.binder import CommentSyntax
from nirjas.output import ScanOutput, MultiLine


def cssExtractor(file):
    """
    Extract comments from CSS file.
    :param file: File to scan
    :type file: string
    :return: Scan output
    :rtype: ScanOutput
    """
    result = CommentSyntax()
    multiline_comment = result.slashStar(file)
    file = file.split("/")
    output = ScanOutput()
    output.filename = file[-1]
    output.lang = "CSS"
    output.total_lines = multiline_comment[4]
    output.total_lines_of_comments = multiline_comment[3]
    output.blank_lines = multiline_comment[5]

    try:
        for idx, _ in enumerate(multiline_comment[0]):
            output.multi_line_comment.append(
                MultiLine(
                    multiline_comment[0][idx],
                    multiline_comment[1][idx],
                    multiline_comment[2][idx],
                )
            )
    except BaseException:
        pass

    return output


def cssSource(file, new_file: str):
    """
    Extract source from CSS file and put at new_file.
    :param file: File to process
    :type file: string
    :param new_file: File to put source at
    :type new_file: string
    :return: Path to new file
    :rtype: string
    """
    copy = True
    with open(new_file, "w+") as f1:
        with open(file) as f:
            for line in f:
                content = ""
                found = False
                if "/*" in line:
                    pos = line.find("/*")
                    content = line[:pos].rstrip()
                    line = line[pos:]
                    copy = False
                    found = True
                if "*/" in line:
                    content = content + line[line.rfind("*/") + 2:]
                    line = content
                    copy = True
                    found = True
                if not found:
                    content = line
                if copy and content.strip() != "":
                    f1.write(content)
    f.close()
    f1.close()
    return new_file
