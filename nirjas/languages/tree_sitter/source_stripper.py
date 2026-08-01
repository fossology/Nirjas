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

from nirjas.languages.language_config import LanguageConfig
from nirjas.languages.language_handlers import get_handler
from nirjas.languages.parser_cache import get_cached_parser_for_config, parse_file
from nirjas.languages.tree_sitter.comment_span import CommentSpan
from nirjas.languages.tree_sitter.comment_visitor import collect_comment_spans


def strip_source(syntax: LanguageConfig, file_path: str, output_path: str) -> str:
    """Remove comments from a source file and write the stripped source."""

    with open(file_path, encoding="utf-8", errors="replace") as source_file:
        source_text = source_file.read()

    parser = get_cached_parser_for_config(syntax, file_path)
    syntax_tree, source_bytes = parse_file(parser, source_text)
    spans = collect_comment_spans(
        syntax_tree.root_node,
        source_bytes,
        syntax,
        get_handler(syntax.handler_name),
    )

    ranges = _expanded_ranges(source_bytes, spans)
    stripped_source = _remove_ranges(source_bytes, ranges).decode(
        "utf-8",
        errors="replace",
    )

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(stripped_source)

    return output_path


def _expanded_ranges(
    source_bytes: bytes,
    spans: list[CommentSpan],
) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for span in spans:
        if _is_shebang_comment(source_bytes, span):
            continue
        ranges.append(_expand_standalone_line(source_bytes, span.start_byte, span.end_byte))
    return _merge_ranges(ranges)


def _is_shebang_comment(source_bytes: bytes, span: CommentSpan) -> bool:
    return span.start_byte == 0 and source_bytes.startswith(b"#!")


def _expand_standalone_line(
    source_bytes: bytes,
    start_byte: int,
    end_byte: int,
) -> tuple[int, int]:
    line_start = source_bytes.rfind(b"\n", 0, start_byte) + 1
    next_newline = source_bytes.find(b"\n", end_byte)
    if next_newline == -1:
        line_end = len(source_bytes)
        removal_end = line_end
    else:
        line_end = next_newline
        removal_end = next_newline + 1

    before = source_bytes[line_start:start_byte]
    after = source_bytes[end_byte:line_end]
    if before.strip() == b"" and after.strip() == b"":
        return line_start, removal_end

    return start_byte, end_byte


def _merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged: list[tuple[int, int]] = []
    for start, end in sorted(ranges):
        if start >= end:
            continue
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
            continue
        previous_start, previous_end = merged[-1]
        merged[-1] = (previous_start, max(previous_end, end))
    return merged


def _remove_ranges(source_bytes: bytes, ranges: list[tuple[int, int]]) -> bytes:
    output = bytearray()
    cursor = 0
    for start, end in ranges:
        output.extend(source_bytes[cursor:start])
        cursor = end
    output.extend(source_bytes[cursor:])
    return bytes(output)
