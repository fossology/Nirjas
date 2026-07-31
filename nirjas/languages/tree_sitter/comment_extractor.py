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

import os
from codecs import BOM_UTF8
from dataclasses import dataclass
from typing import Sequence

from nirjas.languages.language_config import LanguageConfig
from nirjas.languages.language_handlers import get_handler
from nirjas.languages.parser_cache import get_cached_parser_for_config, parse_file
from nirjas.languages.tree_sitter.comment_span import CommentSpan
from nirjas.languages.tree_sitter.comment_visitor import collect_comment_spans
from nirjas.output import MultiLine, SingleLine
from nirjas.output import ScanOutput


_WHITESPACE_BYTES = frozenset(b" \t\r\x0b\x0c")


@dataclass(frozen=True)
class _CommentRecord:
    start_line: int
    end_line: int
    comment: str
    category: str


def extract_comments(syntax: LanguageConfig, file_path: str) -> ScanOutput:
    """Extract comments from a source file using the shared Tree-Sitter pipeline."""

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

    records = [_span_to_record(span, syntax) for span in spans]
    records.sort(key=lambda entry: (entry.start_line, entry.end_line, entry.category))

    single_line_comments = [record for record in records if record.category == "single"]
    multi_line_comments = [record for record in records if record.category == "multi"]

    if syntax.group_contiguous_single_lines:
        single_line_comments, grouped_single_line_comments = (
            _group_contiguous_single_line_comments(single_line_comments)
        )
    else:
        grouped_single_line_comments = []

    total_lines, blank_lines, comment_lines = _count_line_buckets(source_bytes, spans)

    output = ScanOutput()
    output.filename = os.path.basename(file_path)
    output.lang = syntax.display_language
    output.total_lines = total_lines
    output.blank_lines = blank_lines
    output.total_lines_of_comments = comment_lines

    for entry in single_line_comments:
        output.single_line_comment.append(SingleLine(entry.start_line, entry.comment))

    for start_line, end_line, comment in grouped_single_line_comments:
        output.cont_single_line_comment.append(MultiLine(start_line, end_line, comment))

    for entry in multi_line_comments:
        output.multi_line_comment.append(
            MultiLine(entry.start_line, entry.end_line, entry.comment)
        )

    return output


def _count_line_buckets(
    source_bytes: bytes,
    spans: Sequence[CommentSpan],
) -> tuple[int, int, int]:
    """Sort every line into exactly one bucket: blank, comment, or code.

    This follows the convention `cloc` and friends use, so the counts line up
    with what people expect from a line counter:

    The rules, and where the established counters agree with them:

    * a line with no content is blank, even sitting inside a comment block.
      `cloc` agrees; `tokei` and `scc` call it a comment. A line with nothing
      on it is not documentation, and a field named `blank_lines` should count
      empty lines, so we follow `cloc`.
    * a `#!` shebang counts as code. `cloc` agrees; `tokei` and `scc` call it a
      comment. Delete the line and the script stops being executable, so it is
      load-bearing rather than commentary.
    * a line carrying both code and a comment counts as code. Every counter
      agrees, including for a block comment that closes partway through the
      line and leaves code after the `*/`.

    That last case is the one place we knowingly differ from `cloc`, which
    counts `*/ int b = 2;` as a comment even though it holds a statement.
    `cloc` documents mixed lines as code and treats the discrepancy as a defect
    (AlDanial/cloc#875), and `scc` counts it as code, so the divergence is
    deliberate: classifying executable code as comment understates `sloc`.

    Where `cloc` is simply wrong we do not follow it at all. It reads comment
    tokens inside string literals as real comments, so it calls `a = "/*"` a
    comment line; `tokei`, `scc` and Nirjas all count it as code. That is the
    false-positive class this Tree-Sitter migration exists to remove.

    Because each line lands in one bucket, blank + comment + `sloc` always adds
    back up to `total_lines`.
    """

    is_comment_byte = bytearray(len(source_bytes))
    for span in spans:
        start = max(span.start_byte, 0)
        end = min(span.end_byte, len(source_bytes))
        for offset in range(start, end):
            is_comment_byte[offset] = 1

    # A byte-order mark is encoding metadata, not code sitting on line 1.
    content_start = len(BOM_UTF8) if source_bytes.startswith(BOM_UTF8) else 0

    lines = source_bytes.split(b"\n")
    # A trailing newline leaves one empty element behind, which is not a line.
    if lines and lines[-1] == b"":
        lines.pop()

    blank_lines = 0
    comment_lines = 0
    line_start = 0

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            blank_lines += 1
        elif _is_comment_line(
            line,
            line_number,
            line_start,
            content_start,
            is_comment_byte,
        ):
            comment_lines += 1
        line_start += len(line) + 1  # step over the newline itself

    return len(lines), blank_lines, comment_lines


def _is_comment_line(
    line: bytes,
    line_number: int,
    line_start: int,
    content_start: int,
    is_comment_byte: bytearray,
) -> bool:
    """Decide whether a non-blank line counts as comment rather than code."""

    if line_number == 1 and line[content_start:].startswith(b"#!"):
        return False

    return not _has_code_outside_comments(
        line,
        line_start,
        content_start,
        is_comment_byte,
    )


def _has_code_outside_comments(
    line: bytes,
    line_start: int,
    content_start: int,
    is_comment_byte: bytearray,
) -> bool:
    """True when the line holds non-whitespace that no comment span covers."""

    for index, byte_value in enumerate(line):
        offset = line_start + index
        if offset < content_start or is_comment_byte[offset]:
            continue
        if byte_value not in _WHITESPACE_BYTES:
            return True
    return False


def _span_to_record(span: CommentSpan, syntax: LanguageConfig) -> _CommentRecord:
    category = _infer_comment_category(span, syntax)
    if span.is_documentation or category == "multi":
        clean_comment = _strip_multi_line_delimiters(
            span.raw_text,
            syntax.multi_line_delimiters,
        )
        category = "multi"
    else:
        clean_comment = _strip_single_line_prefix(
            span.raw_text,
            syntax.single_line_prefixes,
        )

    return _CommentRecord(
        start_line=span.start_line,
        end_line=span.end_line,
        comment=clean_comment,
        category=category,
    )


def _infer_comment_category(span: CommentSpan, syntax: LanguageConfig) -> str:
    stripped = span.raw_text.strip()
    if span.is_documentation:
        return "multi"

    # Order matters: "multiline_comment" also contains "line_comment", so the
    # block kinds have to be ruled out first (Kotlin, Swift name blocks that way).
    kind_lower = span.node_kind.lower()
    if "block_comment" in kind_lower or "multiline_comment" in kind_lower:
        return "multi"
    if "line_comment" in kind_lower:
        return "single"

    for start_delimiter, _ in sorted(
        syntax.multi_line_delimiters,
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        if stripped.startswith(start_delimiter):
            return "multi"

    if span.start_line != span.end_line:
        return "multi"

    return "single"


def _collapse_multiline_text(text: str) -> str:
    parts = [part.strip() for part in text.splitlines()]
    return " ".join([part for part in parts if part]).strip()


def _strip_single_line_prefix(text: str, prefixes: Sequence[str]) -> str:
    stripped = text.strip()
    for prefix in sorted(prefixes, key=len, reverse=True):
        if not stripped.startswith(prefix):
            continue

        if prefix == "#":
            return stripped.lstrip("#").strip()

        return stripped[len(prefix):].strip()

    return stripped


def _strip_multi_line_delimiters(
    text: str,
    delimiters: Sequence[tuple[str, str]],
) -> str:
    stripped = text.strip()
    for start_delimiter, end_delimiter in sorted(
        delimiters,
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        if stripped.startswith(start_delimiter):
            stripped = stripped[len(start_delimiter):]
            stripped = stripped.strip()
            if end_delimiter and stripped.endswith(end_delimiter):
                stripped = stripped[: -len(end_delimiter)]
            break
    return _collapse_multiline_text(stripped)


def _group_contiguous_single_line_comments(
    single_line_comments: list[_CommentRecord],
) -> tuple[list[_CommentRecord], list[tuple[int, int, str]]]:
    if not single_line_comments:
        return [], []

    grouped_comments: list[tuple[int, int, str]] = []
    remaining_single_comments: list[_CommentRecord] = []
    current_group: list[_CommentRecord] = [single_line_comments[0]]

    for comment in single_line_comments[1:]:
        previous = current_group[-1]
        if comment.start_line == previous.start_line + 1:
            current_group.append(comment)
            continue

        _append_comment_group(
            current_group,
            grouped_comments,
            remaining_single_comments,
        )
        current_group = [comment]

    _append_comment_group(
        current_group,
        grouped_comments,
        remaining_single_comments,
    )
    return remaining_single_comments, grouped_comments


def _append_comment_group(
    current_group: list[_CommentRecord],
    grouped_comments: list[tuple[int, int, str]],
    remaining_single_comments: list[_CommentRecord],
) -> None:
    if len(current_group) > 1:
        grouped_comments.append(
            (
                current_group[0].start_line,
                current_group[-1].start_line,
                "".join(f" {entry.comment}" for entry in current_group),
            )
        )
    else:
        remaining_single_comments.append(current_group[0])
