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

from nirjas.output import ScanOutput, MultiLine


def textExtractor(file):
    content = ""
    total_lines, blank_lines = 0, 0
    with open(file) as f:
        for line_number, line in enumerate(f, start=1):
            total_lines += 1
            line = line.strip()
            content = content + line.replace('\n', ' ')
            if line == '':
                blank_lines += 1

    file = file.split('/')

    output = ScanOutput()
    output.filename = file[-1]
    output.lang = 'text'
    output.total_lines = total_lines
    output.total_lines_of_comments = total_lines - blank_lines
    output.blank_lines = blank_lines

    output.multi_line_comment.append(MultiLine(1, total_lines, content))

    return output
