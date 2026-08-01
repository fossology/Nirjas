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

from typing import Protocol, runtime_checkable


@runtime_checkable
class LanguageHandler(Protocol):
    """Optional per-language hook for docstring and disambiguation logic."""

    def is_documentation_comment(
        self,
        node,
        parent,
        source: str,
    ) -> bool | None:
        """
        Return True if node is a documentation comment, False if explicitly not,
        or None if this handler does not apply to the node.
        """


class DefaultHandler:
    """Baseline handler: exact node kinds are sufficient; no docstring logic."""

    def is_documentation_comment(
        self,
        node,
        parent,
        source: str,
    ) -> bool | None:
        return None


class PythonHandler:
    """
    Python docstring detection ported from uncomment's PythonHandler.

    Handles grammar variants where docstrings appear under expression_statement
    or directly under module/block, and skips leading comment nodes when
    checking is_first_statement.
    """

    _BLOCK_PARENT_KINDS = frozenset(
        {"function_definition", "async_function_definition", "class_definition"}
    )

    def is_documentation_comment(
        self,
        node,
        parent,
        source: str,
    ) -> bool | None:
        if node.type != "string":
            return None

        if parent is None:
            return False

        if parent.type == "expression_statement":
            grandparent = parent.parent
            if grandparent is None:
                return False

            if grandparent.type == "module":
                return self._is_first_statement(parent, grandparent)

            if grandparent.type == "block":
                block_parent = grandparent.parent
                if block_parent is None:
                    return False
                if block_parent.type in self._BLOCK_PARENT_KINDS:
                    return self._is_first_statement(parent, grandparent)
                return False

            return False

        if parent.type == "module":
            return self._is_first_statement(node, parent)

        if parent.type == "block":
            block_parent = parent.parent
            if block_parent is None:
                return False
            if block_parent.type in self._BLOCK_PARENT_KINDS:
                return self._is_first_statement(node, parent)
            return False

        return False

    def _is_first_statement(self, statement, parent) -> bool:
        for index in range(parent.child_count):
            child = parent.child(index)
            if child.type != "comment":
                same_start = child.start_byte == statement.start_byte
                same_end = child.end_byte == statement.end_byte
                return same_start and same_end
        return False


_HANDLERS: dict[str, LanguageHandler] = {
    "python": PythonHandler(),
}


def get_handler(handler_name: str | None) -> LanguageHandler:
    """Return the handler for a language config, defaulting to DefaultHandler."""

    if handler_name is None:
        return DefaultHandler()
    return _HANDLERS.get(handler_name, DefaultHandler())
