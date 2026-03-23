#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPDX-License-Identifier: LGPL-2.1

Base tree-sitter extractor for comment extraction.
"""

from __future__ import annotations

import os
from itertools import groupby
from operator import itemgetter
from typing import Literal, NamedTuple

from nirjas.output import MultiLine, ScanOutput, SingleLine

_Classification = Literal["single", "multi", None]


class _CommentNode(NamedTuple):
    kind: str
    start_line: int
    end_line: int
    text: str


class TreeSitterExtractor:
    """
    Base class for tree-sitter comment extractors.

    Subclasses must implement :meth:`classify_node` to tell the traversal
    engine whether a given tree-sitter node is a *single-line* comment,
    a *multi-line* comment, or should be ignored.

    Parser instances are cached at the class level so that one parser object
    is reused for all files processed by the same extractor type.

    Parameters
    ----------
    language_name:
        The tree-sitter language identifier (e.g. ``"python"``).
    """

    _parser_cache: dict = {}

    def __init__(self, language_name: str) -> None:
        self.language_name = language_name

    def _get_parser(self):
        """Return (and cache) the tree-sitter parser for this language."""
        if self.language_name not in TreeSitterExtractor._parser_cache:
            from tree_sitter_language_pack import download, downloaded_languages, get_parser
            if self.language_name not in downloaded_languages():
                download([self.language_name])
            TreeSitterExtractor._parser_cache[self.language_name] = get_parser(
                self.language_name
            )
        return TreeSitterExtractor._parser_cache[self.language_name]

    def classify_node(self, node) -> _Classification:
        """
        Classify a tree-sitter node as a comment kind.

        Returns
        -------
        ``"single"``
            The node represents a single-line comment (or a multi-line string
            that fits on one line and should be treated as single).
        ``"multi"``
            The node represents a multi-line comment.
        ``None``
            The node is not a comment; continue tree traversal into children.
        """
        raise NotImplementedError

    def _collect(self, node, results: list[_CommentNode]) -> None:
        """DFS traversal that collects all comment nodes."""
        classification = self.classify_node(node)

        if classification in ("single", "multi"):
            start = node.start_point[0] + 1   # tree-sitter is 0-based
            end = node.end_point[0] + 1
            text = node.text.decode("utf-8", errors="replace")
            results.append(_CommentNode(classification, start, end, text))
            return

        for child in node.children:
            self._collect(child, results)

    @staticmethod
    def _group_consecutive(
        singles: list[_CommentNode],
    ) -> tuple[list[_CommentNode], list[_CommentNode]]:
        """
        Split *singles* into isolated comments and consecutively-grouped ones.

        Returns
        -------
        isolated : list[_CommentNode]
            Comments whose adjacent lines are NOT also comments.
        groups : list[_CommentNode]
            One merged :class:`_CommentNode` per consecutive run of 2+ comments,
            with the combined text matching the format produced by
            ``binder.contSingleLines`` (space-joining with a leading space).
        """
        if not singles:
            return [], []

        by_line: dict[int, str] = {c.start_line: c.text for c in singles}
        line_numbers = sorted(by_line)

        isolated: list[_CommentNode] = []
        groups: list[_CommentNode] = []

        for _, run in groupby(
            enumerate(line_numbers), lambda x: x[0] - x[1]
        ):
            run_lines = list(map(itemgetter(1), run))
            if len(run_lines) == 1:
                ln = run_lines[0]
                isolated.append(_CommentNode("single", ln, ln, by_line[ln]))
            else:
                start = run_lines[0]
                end = run_lines[-1]
                # Replicate binder.contSingleLines concatenation (leading space)
                combined = "".join(" " + by_line[ln] for ln in run_lines)
                groups.append(_CommentNode("multi", start, end, combined))

        return isolated, groups

    def build_scan_output(self, filepath: str, lang: str) -> ScanOutput:
        """
        Parse *filepath* and return a populated :class:`ScanOutput`.

        Parameters
        ----------
        filepath:
            Absolute (or relative) path to the source file.
        lang:
            Human-readable language name stored in the metadata, e.g.
            ``"Python"``.
        """
        with open(filepath, "rb") as fh:
            source_bytes = fh.read()

        # Normalise Windows (CRLF) and old Mac (CR) line endings so that
        # comment text does not contain stray \r characters.
        source_bytes = source_bytes.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

        source_text = source_bytes.decode("utf-8", errors="replace")
        lines = source_text.splitlines()
        total_lines = len(lines)
        blank_lines = sum(1 for ln in lines if ln.strip() == "")

        parser = self._get_parser()
        tree = parser.parse(source_bytes)

        raw: list[_CommentNode] = []
        self._collect(tree.root_node, raw)

        singles = [c for c in raw if c.kind == "single"]
        multis = sorted(
            [c for c in raw if c.kind == "multi"], key=lambda c: c.start_line
        )

        isolated, cont_groups = self._group_consecutive(
            sorted(singles, key=lambda c: c.start_line)
        )

        total_lines_of_comments = len(singles) + sum(
            c.end_line - c.start_line + 1 for c in multis
        )

        filename = os.path.basename(filepath)

        output = ScanOutput()
        output.filename = filename
        output.lang = lang
        output.total_lines = total_lines
        output.total_lines_of_comments = total_lines_of_comments
        output.blank_lines = blank_lines

        for c in isolated:
            output.single_line_comment.append(SingleLine(c.start_line, c.text))

        for c in cont_groups:
            output.cont_single_line_comment.append(
                MultiLine(c.start_line, c.end_line, c.text)
            )

        for c in multis:
            output.multi_line_comment.append(
                MultiLine(c.start_line, c.end_line, c.text)
            )

        return output
