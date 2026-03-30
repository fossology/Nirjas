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

from nirjas.languages._base import TreeSitterExtractor

_TRIPLE_QUOTE_OPENINGS = ('"""', "'''")
_STRING_PREFIXES = frozenset("rRbBuUfF")


def _is_triple_quoted(node) -> bool:
    text: str = node.text.decode("utf-8", errors="replace")
    i = 0
    while i < len(text) and text[i] in _STRING_PREFIXES:
        i += 1
    rest = text[i:]
    return rest.startswith(_TRIPLE_QUOTE_OPENINGS[0]) or rest.startswith(_TRIPLE_QUOTE_OPENINGS[1])


class _PythonExtractor(TreeSitterExtractor):
    def __init__(self) -> None:
        super().__init__("python")

    def classify_node(self, node):
        if node.type == "comment":
            return "single"

        if node.type == "string" and _is_triple_quoted(node):
            start = node.start_point[0]
            end = node.end_point[0]
            return "single" if start == end else "multi"

        return None


_EXTRACTOR = _PythonExtractor()


def pythonExtractor(file):
    """
    Extract comments from Python file.
    :param file: File to scan
    :type file: string
    :return: Scan output
    :rtype: ScanOutput
    """
    return _EXTRACTOR.build_scan_output(file, "Python")


def pythonSource(file, new_file: str):
    """
    Extract source from Python file and put at new_file.
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
                if '"""' in line:
                    if copy:
                        pos = line.find('"""')
                        content = line[:pos].rstrip()
                        line = line[pos:]
                        copy = False
                        found = True
                    else:
                        content = content + line[line.rfind('"""') + 3 :]
                        line = content
                        copy = True
                        found = True
                if "'''" in line:
                    if copy:
                        pos = line.find("'''")
                        content = line[:pos].rstrip()
                        line = line[pos:]
                        copy = False
                        found = True
                    else:
                        content = content + line[line.rfind("'''") + 3 :]
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
