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
from nirjas.output import ScanOutput, SingleLine


def rExtractor(file):
    result = CommentSyntax()
    single_line_comment = result.hash(file)
    file = file.split("/")
    output = ScanOutput()
    output.filename = file[-1]
    output.lang = 'R'
    output.total_lines = single_line_comment[1]
    output.total_lines_of_comments = single_line_comment[3]
    output.blank_lines = single_line_comment[2]

    for i in single_line_comment[0]:
        output.single_line_comment.append(SingleLine(i[0], i[1]))

    return output


def rSource(file, new_file: str):
    with open(new_file, 'w+') as f1:
        with open(file) as f:
            for line in f:
                content = line
                if '#' in line:
                    content = line[:line.find('#')].rstrip() + '\n'
                if content.strip() != '':
                    f1.write(content)
    f.close()
    f1.close()
    return new_file
