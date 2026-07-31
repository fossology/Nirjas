#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (C) 2020  Ayush Bhardwaj (classicayush@gmail.com),
Kaushlendra Pratap (kaushlendrapratap.9837@gmail.com)
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


RUST_CONFIG = LanguageConfig(
    display_language="Rust",
    parser_language="rust",
    comment_node_kinds=frozenset({"block_comment", "doc_comment", "inner_doc_comment", "line_comment", "outer_doc_comment"}),
    doc_comment_node_kinds=frozenset({"doc_comment", "inner_doc_comment", "outer_doc_comment"}),
    single_line_prefixes=("///", "//!", "//",),
    multi_line_delimiters=(("/*", "*/"),),
)


def rustExtractor(file):
    return RUST_CONFIG.extract(file)


def rustSource(file, new_file: str):
    return RUST_CONFIG.strip_source(file, new_file)
