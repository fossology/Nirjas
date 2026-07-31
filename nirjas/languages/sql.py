#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (C) Sushant Kumar (sushantmishra02102002@gmail.com)
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


SQL_CONFIG = LanguageConfig(
    display_language="SQL",
    parser_language="sql",
    # The SQL grammar names `--` line comments `marginalia`; without it only
    # the `/* */` blocks are detected.
    comment_node_kinds=frozenset({"comment", "marginalia"}),
    single_line_prefixes=("--",),
    multi_line_delimiters=(("/*", "*/"),),
)


def sqlExtractor(file):
    return SQL_CONFIG.extract(file)


def sqlSource(file, new_file: str):
    return SQL_CONFIG.strip_source(file, new_file)
