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


def pythonExtractor(file):
    result = CommentSyntax()
    result1 = result.hash(file)
    result2 = result.singleQuotes(file)
    result3 = result.doubleQuotes(file)
    file = file.split("/")
    output = {
        "metadata": [{
        "filename": file[-1],
        "lang": "Python",
        "total_lines": result1[1],
        "total_lines_of_comments": result1[3]+result2[3]+result3[3],
        "blank_lines": result1[2],
        "sloc": result1[1]-(result1[3]+result2[3]+result3[3]+result1[2])
        }],
        "single_line_comment": [],
        "multi_line_comment": []
    }
    if result1:
        for i in result1[0]:
            output['single_line_comment'].append({"line_number" :i[0],"comment": i[1]})

    if result2:
        for idx,i in enumerate(result2[0]):
            output['multi_line_comment'].append({"start_line": result2[0][idx], "end_line": result2[1][idx], "comment": result2[2][idx]})
        
    if result3:
        for idx,i in enumerate(result3[0]):
            output['multi_line_comment'].append({"start_line": result2[0][idx], "end_line": result2[1][idx], "comment": result2[2][idx]})

    return output


def pythonSource(file, newFile: str):
    closingCount = 0
    copy = True
    with open(newFile, 'w+') as f1:
        with open(file) as f:
            for lineNumber, line in enumerate(f, start=1):
                if line.strip() == "'''":
                    closingCount+=1
                    copy = False
                    if closingCount%2 == 0:
                        copy = True

                if line.strip() == '"""':
                    closingCount+=1
                    copy = False
                    if closingCount%2 == 0:
                        copy = True

                if copy:
                    if line.strip() != "'''" and line.strip() != '"""':
                        Templine = line.replace(" ","")
                        if Templine[0] != "#":            # Syntax for single line comment
                            f1.write(line)
    f.close()
    f1.close()
    return newFile
    