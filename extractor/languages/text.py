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

def textExtractor(file):
    result1 = []
    content = ""
    total_lines, blank_lines = 0,0
    with open(file) as f:
        for lineNumber, line in enumerate(f, start=1):
            total_lines += 1
            content = content + line.replace('\n',' ')
            if not line.strip():
                blank_lines += 1

    result1.append(content)


    file = file.split("/")
    output = {
        "metadata": [{
        "filename": file[-1],
        "lang": "text",
        "total_lines": total_lines,
        "total_lines_of_comments": total_lines-blank_lines,
        "blank_lines": blank_lines,
        "sloc": 0,
        }],
        "single_line_comment": [],
        "multi_line_comment": []
    }

    if result1 :
        output['multi_line_comment'].append({"start_line": 1, "end_line": total_lines, "comment": result1[0]})
    
    return output

