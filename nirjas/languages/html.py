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

from nirjas.binder import *
from nirjas.output import ScanOutput, MultiLine


def htmlExtractor(file):
    result = CommentSyntax()
    multiline_dash_comment = result.gtExclamationDash(file)
    multiline_star_comment = result.slashStar(file)
    file = file.split("/")
    output = ScanOutput()
    output.filename = file[-1]
    output.lang = 'HTML'
    output.total_lines = multiline_dash_comment[4]
    output.total_lines_of_comments = multiline_dash_comment[3] + multiline_star_comment[3]
    output.blank_lines = multiline_dash_comment[5]

    try:
        for idx, i in enumerate(multiline_dash_comment[0]):
            output.multi_line_comment.append(MultiLine(
                multiline_dash_comment[0][idx], multiline_dash_comment[1][idx],
                multiline_dash_comment[2][idx]))
    except:
        pass

    try:
        for idx, i in enumerate(multiline_star_comment[0]):
            output.multi_line_comment.append(MultiLine(
                multiline_star_comment[0][idx], multiline_star_comment[1][idx],
                multiline_star_comment[2][idx]))
    except:
        pass

    return output


def htmlSource(file, new_file: str):
    copy = True
    with open(new_file, 'w+') as f1:
        with open(file) as f:
            for line in f:
                content = ""
                found = False
                if '/*' in line:
                    pos = line.find('/*')
                    content = line[:pos].rstrip()
                    line = line[pos:]
                    copy = False
                    found = True
                if '*/' in line:
                    content = content + line[line.rfind('*/') + 2:]
                    line = content
                    copy = True
                    found = True
                if '<!--' in line:
                    pos = line.find('<!--')
                    content = line[:pos].rstrip()
                    line = line[pos:]
                    copy = False
                    found = True
                if '-->' in line:
                    content = content + line[line.rfind('-->') + 3:]
                    line = content
                    copy = True
                    found = True
                if not found:
                    content = line
                if copy and content.strip() != '':
                    f1.write(content)
    f.close()
    f1.close()
    return new_file
