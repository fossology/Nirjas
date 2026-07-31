#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (C) 2020  Aman Dwivedi (aman.dwivedi5@gmail.com)
Copyright (C) 2026  Swapnil Dutta (swapnil@rycerz.es)

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


from nirjas.languages.language_config import LanguageConfig


SCSS_CONFIG = LanguageConfig(
    display_language="Scss",
    parser_language="scss",
    # The SCSS grammar reports `//` line comments as `js_comment`, so leaving
    # it out silently drops every single-line comment in the file.
    comment_node_kinds=frozenset({"comment", "js_comment"}),
    single_line_prefixes=("///", "//",),
    multi_line_delimiters=(("/*", "*/"),),
)


def scssExtractor(file):
    return SCSS_CONFIG.extract(file)


def scssSource(file, new_file: str):
    return SCSS_CONFIG.strip_source(file, new_file)
