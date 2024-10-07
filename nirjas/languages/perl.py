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


def perlExtractor(file):
    """
    Extract comments from Perl file.
    :param file: File to scan
    :type file: string
    :return: Scan output
    :rtype: ScanOutput
    """
    result = CommentSyntax()
    single_line_comment = result.hash(file)
    multiline_comment = result.beginCut(file)
    cont_single_line_comment = contSingleLines(single_line_comment)
    file = file.split("/")
    output = ScanOutput()
    output.filename = file[-1]
    output.lang = "Perl"
    output.total_lines = single_line_comment[1]
    output.total_lines_of_comments = single_line_comment[3] + multiline_comment[3]
    output.blank_lines = single_line_comment[2]

    if cont_single_line_comment:
        single_line_comment = cont_single_line_comment[0]

    for i in single_line_comment[0]:
        output.single_line_comment.append(SingleLine(i[0], i[1]))

    for idx, i in enumerate(cont_single_line_comment[1]):
        output.cont_single_line_comment.append(
            MultiLine(
                cont_single_line_comment[1][idx],
                cont_single_line_comment[2][idx],
                cont_single_line_comment[3][idx],
            )
        )

    for idx, i in enumerate(multiline_comment[0]):
        output.multi_line_comment.append(
            MultiLine(
                multiline_comment[0][idx],
                multiline_comment[1][idx],
                multiline_comment[2][idx],
            )
        )

    return output


def perlSource(file, new_file: str):
    """
    Extract source from Perl file and put at new_file.
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
                if "=begin" in line:
                    pos = line.find("=begin")
                    content = line[:pos].rstrip()
                    line = line[pos:]
                    copy = False
                    found = True
                if "=cut" in line:
                    content = content + line[line.rfind("=cut") + 4 :]
                    line = content
                    copy = True
                    found = True
                if "#" in line:
                    content = line[: line.find("#")].rstrip() + "\n"
                    found = True
                if not found:
                    content = line
                if copy and content.strip() != "":
                    f1.write(content)
    f.close()
    f1.close()
    return new_file
