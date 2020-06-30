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

from binder import readSingleLine, readMultiLineSame, readMultiLineDiff, CommentSyntax

def shellExtractor(file):
    result = CommentSyntax()
    result1 = result.hash(file)
    file = file.split("/")
    output = {
        "metadata": [{
        "filename": file[-1],
        "lang": "Shell",
        "total_lines": result1[1],
        "total_lines_of_comments": result1[3],
        "blank_lines": result1[2],
        "sloc": result1[1]-(result1[3]+result1[2])
        }],
        "single_line_comment": [],
        "multi_line_comment": []
    }
    if result1:
        for i in result1[0]:
            output['single_line_comment'].append({"line_number" :i[0],"comment": i[1]})


    return output


def shellSource(file, newFile: str):
    closingCount = 0
    copy = True
    with open(newFile, 'w+') as f1:
        with open(file) as f:
            for lineNumber, line in enumerate(f, start=1):
                Templine = line.replace(" ","")
                if Templine[0] != "#":            # Syntax for single line comment
                    f1.write(line)
    f.close()
    f1.close()
    return newFile