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
from typing import Any

from nirjas.language_registry import parser_name, parser_name_for_path
from nirjas.languages.language_config import LanguageConfig

try:
    from tree_sitter_language_pack import get_parser  # pyright: ignore[reportMissingImports]
except ImportError as exc:  # pragma: no cover - handled at runtime
    get_parser = None
    _IMPORT_ERROR = exc
else:  # pragma: no cover - simple assignment
    _IMPORT_ERROR = None

_PARSER_CACHE: dict[str, object] = {}


def get_cached_parser(nirjas_language: str):
    """Get a cached Tree-Sitter parser for a nirjas language name."""

    return _get_cached_parser_by_name(parser_name(nirjas_language))


def get_cached_parser_for_path(path: str):
    """Get a cached Tree-Sitter parser resolved from a file path."""

    return _get_cached_parser_by_name(parser_name_for_path(path))


def get_cached_parser_for_config(syntax: LanguageConfig, path: str):
    """Get a cached parser using config defaults plus extension-specific overrides."""

    extension = os.path.splitext(path)[1]
    parser_language = syntax.parser_language_by_extension.get(
        extension,
        syntax.parser_language,
    )
    return _get_cached_parser_by_name(parser_name(parser_language))


def _get_cached_parser_by_name(parser_language: str):
    if get_parser is None:
        raise RuntimeError(
            "tree-sitter-language-pack is required for comment extraction. "
            "Install dependencies with: pip install ."
        ) from _IMPORT_ERROR

    parser = _PARSER_CACHE.get(parser_language)
    if parser is None:
        parser = get_parser(parser_language)
        _PARSER_CACHE[parser_language] = parser
    return parser


def parse_file(parser: Any, source_text: str) -> tuple[Any, bytes]:
    """Parse source text and return the syntax tree plus UTF-8 bytes for slicing."""

    source_bytes = source_text.encode("utf-8", errors="replace")
    return parser.parse(source_bytes), source_bytes
