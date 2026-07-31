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

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from nirjas.output import ScanOutput


@dataclass(frozen=True)
class LanguageConfig:
    """Per-language comment rules for Tree-Sitter extraction and source stripping."""

    display_language: str
    parser_language: str
    comment_node_kinds: frozenset[str]
    doc_comment_node_kinds: frozenset[str] = frozenset()
    single_line_prefixes: tuple[str, ...] = ()
    multi_line_delimiters: tuple[tuple[str, str], ...] = ()
    group_contiguous_single_lines: bool = True
    handler_name: str | None = None
    parser_language_by_extension: dict[str, str] = field(default_factory=dict)

    def extract(self, file_path: str) -> ScanOutput:
        """Extract comments from a source file."""

        from nirjas.languages.tree_sitter.comment_extractor import extract_comments

        return extract_comments(self, file_path)

    def strip_source(self, file_path: str, output_path: str) -> str:
        """Remove comments from a source file and write the result."""

        from nirjas.languages.tree_sitter.source_stripper import strip_source

        return strip_source(self, file_path, output_path)
