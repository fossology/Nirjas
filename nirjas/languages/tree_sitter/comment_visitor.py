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

import warnings

from nirjas.languages.language_config import LanguageConfig
from nirjas.languages.language_handlers import LanguageHandler
from nirjas.languages.tree_sitter.comment_span import CommentSpan


class UnverifiedQuotedParentWarning(UserWarning):
    """A comment node sat under a quoting construct Nirjas has not audited.

    Tree-Sitter exposes no cross-grammar notion of "this node is quoted text":
    node kinds are named by each grammar author, and nothing in the API marks a
    rule as a string. So the check below is necessarily name-based, and this
    warning is how a name Nirjas has never verified announces itself instead of
    silently deciding the outcome. Raise it to an exception with::

        -W error::nirjas.languages.tree_sitter.comment_visitor.UnverifiedQuotedParentWarning

    See :data:`QUOTED_PARENT_NODE_KINDS` for what to do about one.
    """


#: Parent node kinds that mean a "comment" node is really quoted text.
#:
#: Some grammars emit a comment node *inside* a string literal or a quoted
#: attribute value, where the delimiters are data rather than commentary:
#:
#:   * tree-sitter-swift parses `let s = "/* x */"` into a `multiline_comment`
#:     that is a direct child of `line_string_literal`. A `//` in the same
#:     position correctly yields `line_str_text` instead.
#:   * tree-sitter-html parses `<p title="<!-- x -->">` into a `comment` that is
#:     a direct child of `quoted_attribute_value`.
#:
#: Reporting those as comments is the false-positive class this migration exists
#: to remove, and it also made `Source()` delete the contents of the string it
#: was supposed to preserve.
#:
#: Every kind here has been confirmed against the grammar that emits it, so a
#: match suppresses the comment silently. Kinds that only *look* quoted are
#: handled by :func:`kind_looks_quoted` and warn, because the set cannot
#: enumerate grammars nobody has read yet -- new languages, and upstream
#: grammars that rename a rule in a release.
#:
#: Only the *immediate* parent is checked, deliberately. A genuine comment
#: written inside an interpolation hangs off the substitution node rather than
#: the string itself -- JavaScript ``  `a ${/* real */ 1} b`  `` gives
#: comment -> template_substitution -> template_string -- so walking further up
#: the ancestry would discard real comments.
QUOTED_PARENT_NODE_KINDS = frozenset(
    {
        "line_string_literal",
        "multi_line_string_literal",
        "quoted_attribute_value",
        "attribute_value",
        "raw_string_literal",
        "string_literal",
        "template_string",
        "string",
    }
)

#: Substrings that mark a node kind as a quoting construct.
#:
#: Tree-Sitter grammars are independent projects, but they converge hard on
#: these names for the rule that owns quoted bytes: `string`, `string_literal`,
#: `raw_string_literal`, `interpreted_string_literal`, `line_string_literal`,
#: `template_string`, `heredoc_body`, `quoted_attribute_value`,
#: `quoted_template`, `attribute_value`. Matching the convention is what lets a
#: grammar Nirjas has never seen get the right answer by default; the warning is
#: what stops that default from being invisible.
QUOTED_KIND_MARKERS = ("string", "heredoc", "quoted", "attribute_value")

#: Substrings that mark a node kind as an *interpolation* hole, checked first
#: and overriding :data:`QUOTED_KIND_MARKERS`.
#:
#: The bytes inside `${...}`, `#{...}` or `$(...)` are code, so a comment there
#: is a real comment. Several grammars name the hole after its enclosing string
#: -- `string_interpolation` in Swift and Scala -- and without this precedence
#: the `string` marker would swallow those and delete real comments.
INTERPOLATION_KIND_MARKERS = (
    "interpolation",
    "substitution",
    "expansion",
    "embedded",
)

#: (parser language, comment kind, parent kind) triples already reported, so a
#: scan over a large tree warns once per novel construct rather than per node.
_reported_quoted_parents: set[tuple[str, str, str]] = set()


def reset_unverified_quoted_parent_reports() -> None:
    """Forget which unverified parents have been warned about.

    Only needed by tests, which have to observe a warning the deduplication
    would otherwise suppress after the first scan in the process.
    """

    _reported_quoted_parents.clear()


def kind_looks_quoted(node_kind: str) -> bool:
    """True when a node kind names a quoting construct by naming convention.

    Used for parent kinds outside :data:`QUOTED_PARENT_NODE_KINDS`, where there
    is no audited answer and the name is the only evidence available.
    """

    if any(marker in node_kind for marker in INTERPOLATION_KIND_MARKERS):
        return False
    return any(marker in node_kind for marker in QUOTED_KIND_MARKERS)


def _report_unverified_quoted_parent(
    parser_language: str,
    node_kind: str,
    parent_kind: str,
) -> None:
    key = (parser_language, node_kind, parent_kind)
    if key in _reported_quoted_parents:
        return
    _reported_quoted_parents.add(key)

    warnings.warn(
        f"tree-sitter-{parser_language} emitted a '{node_kind}' node directly "
        f"inside '{parent_kind}', a parent kind that is not in "
        f"QUOTED_PARENT_NODE_KINDS. Its name matches the quoting convention, so "
        f"Nirjas treated the node as quoted text rather than as a comment. "
        f"Confirm that against the grammar and add '{parent_kind}' to "
        f"QUOTED_PARENT_NODE_KINDS in "
        f"nirjas/languages/tree_sitter/comment_visitor.py, so the decision stops "
        f"resting on a heuristic.",
        UnverifiedQuotedParentWarning,
        stacklevel=2,
    )


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

        # A comment token sitting directly inside a quoted literal is that
        # literal's text, not a comment.
        if is_comment and parent is not None:
            parent_kind = parent.type
            if parent_kind in QUOTED_PARENT_NODE_KINDS:
                is_comment = False
            elif kind_looks_quoted(parent_kind):
                # Not audited, so say so rather than deciding in silence.
                _report_unverified_quoted_parent(
                    syntax.parser_language,
                    node_kind,
                    parent_kind,
                )
                is_comment = False
            is_documentation = is_documentation and is_comment

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
