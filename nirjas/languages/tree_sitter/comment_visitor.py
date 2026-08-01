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
from nirjas.languages.language_handlers import LanguageHandler
from nirjas.languages.tree_sitter.comment_span import CommentSpan


def collect_comment_spans(
    root_node,
    source_bytes: bytes,
    syntax: LanguageConfig,
    handler: LanguageHandler,
) -> list[CommentSpan]:
    """Walk a Tree-Sitter tree and collect exact comment/doc-comment spans."""

    spans: list[CommentSpan] = []
    source_text = source_bytes.decode("utf-8", errors="replace")

    def visit(node, parent) -> None:
        node_kind = node.type
        is_documentation = False

        if node_kind in syntax.comment_node_kinds:
            is_comment = True
            is_documentation = node_kind in syntax.doc_comment_node_kinds
        elif node_kind in syntax.doc_comment_node_kinds:
            is_comment = handler.is_documentation_comment(
                node,
                parent,
                source_text,
            )
            is_documentation = bool(is_comment)
        else:
            is_comment = False

        if is_comment:
            start_byte = node.start_byte
            end_byte = node.end_byte
            spans.append(
                CommentSpan(
                    start_byte=start_byte,
                    end_byte=end_byte,
                    start_line=node.start_point.row + 1,
                    end_line=node.end_point.row + 1,
                    node_kind=node_kind,
                    is_documentation=is_documentation,
                    raw_text=source_bytes[start_byte:end_byte].decode(
                        "utf-8",
                        errors="replace",
                    ),
                )
            )

        for index in range(node.child_count):
            visit(node.child(index), node)

    visit(root_node, None)
    spans.sort(key=lambda span: (span.start_byte, span.end_byte, span.node_kind))
    return spans
