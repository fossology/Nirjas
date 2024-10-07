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

from nirjas.binder import CommentSyntax, contSingleLines
from nirjas.output import MultiLine, ScanOutput, SingleLine


def c_sharpExtractor(file):
    """
    Extract comments from C# file.
    :param file: File to scan
    :type file: string
    :return: Scan output
    :rtype: ScanOutput
    """
    result = CommentSyntax()
    single_line_comment = result.doubleSlash(file)
    multiline_comment = result.slashStar(file)
    cont_single_line_comment = contSingleLines(single_line_comment)
    file = file.split("/")
    output = ScanOutput()
    output.filename = file[-1]
    output.lang = "C#"
    output.total_lines = single_line_comment[1]
    output.total_lines_of_comments = single_line_comment[3] + multiline_comment[3]
    output.blank_lines = single_line_comment[2]

    if cont_single_line_comment:
        single_line_comment = cont_single_line_comment[0]

    for i in single_line_comment[0]:
        output.single_line_comment.append(SingleLine(i[0], i[1]))

    for idx, _ in enumerate(cont_single_line_comment[1]):
        output.cont_single_line_comment.append(
            MultiLine(
                cont_single_line_comment[1][idx],
                cont_single_line_comment[2][idx],
                cont_single_line_comment[3][idx],
            )
        )

    for idx, _ in enumerate(multiline_comment[0]):
        output.multi_line_comment.append(
            MultiLine(
                multiline_comment[0][idx],
                multiline_comment[1][idx],
                multiline_comment[2][idx],
            )
        )

    return output


def c_sharpSource(file, new_file: str):
    """
    Extract source from C# file and put at new_file.
    :param file: File to process
    :type file: string
    :param new_file: File to put source at
    :type new_file: string
    :return: Path to new file
    :rtype: string
    """
    copy = True
    with open(new_file, "w+") as f1:
        with open(file, "r") as f:
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
                    content = content + line[line.rfind("*/") + 2 :]
                    line = content
                    copy = True
                    found = True
                if "//" in line:
                    if line[line.find("//") - 1] != ":":
                        line = line[: line.find("//")].rstrip() + "\n"
                    elif line[line.rfind("//") - 1] != ":":
                        line = line[: line.rfind("//")].rstrip() + "\n"
                    content = line
                    found = True
                if not found:
                    content = line
                if copy and content.strip() != "":
                    f1.write(content)
    f.close()
    f1.close()
    return new_file
