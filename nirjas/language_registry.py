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

# Extension → nirjas module name (same semantics as former LanguageMapper.LANG_MAP).
EXTENSION_MAP: dict[str, str] = {
    ".py": "python",
    ".m4": "python",
    ".nsi": "python",
    ".hpp": "cpp",
    ".c": "c",
    ".h": "cpp",
    ".cs": "c_sharp",
    ".cpp": "cpp",
    ".scss": "scss",
    ".sep": "cpp",
    ".hxx": "cpp",
    ".cc": "cpp",
    ".css": "css",
    ".dart": "dart",
    ".go": "go",
    ".hs": "haskell",
    ".html": "html",
    ".xml": "html",
    ".java": "java",
    ".js": "javascript",
    ".jsx": "javascript",
    ".jl": "julia",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".ktm": "kotlin",
    ".m": "matlab",
    ".php": "php",
    ".pl": "perl",
    ".r": "r",
    ".R": "r",
    ".rb": "ruby",
    ".rs": "rust",
    ".sh": "shell",
    ".sql": "sql",
    ".swift": "swift",
    ".scala": "scala",
    ".sc": "scala",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".txt": "text",
    ".lic": "text",
    ".install": "text",
    ".OSS": "text",
    ".gl": "text",
}

# Nirjas module name → Tree-Sitter parser name in tree-sitter-language-pack.
PARSER_ALIASES: dict[str, str] = {
    "c_sharp": "csharp",
    "c#": "csharp",
    "shell": "bash",
    "sh": "bash",
    "shellscript": "bash",
}


class NotSupportedExtension(Exception):
    """Raised when a file extension is not recognized."""

    def __str__(self) -> str:
        return "extension '" + self.args[0] + "' not supported"


def nirjas_name_from_path(path: str) -> str:
    """Return the nirjas language module name for a file path."""

    extension = os.path.splitext(path)[1]
    if extension not in EXTENSION_MAP:
        raise NotSupportedExtension(extension)
    return EXTENSION_MAP[extension]


def parser_name(nirjas_language: str) -> str:
    """Resolve a nirjas language name to a Tree-Sitter parser name."""

    return PARSER_ALIASES.get(nirjas_language, nirjas_language)


def parser_name_for_path(path: str) -> str:
    """Resolve parser name from file path, including extension-specific overrides."""

    nirjas_language = nirjas_name_from_path(path)
    if nirjas_language == "typescript" and path.endswith(".tsx"):
        return "tsx"
    return parser_name(nirjas_language)
