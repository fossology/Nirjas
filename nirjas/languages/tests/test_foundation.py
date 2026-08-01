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
import tempfile
import unittest
from typing import Any

from nirjas.language_registry import (
    NotSupportedExtension,
    nirjas_name_from_path,
    parser_name,
    parser_name_for_path,
)
from nirjas.languages import c, kotlin, python, shell, typescript
from nirjas.languages.language_config import LanguageConfig
from nirjas.languages.language_handlers import DefaultHandler, PythonHandler, get_handler
from nirjas.languages.parser_cache import get_cached_parser_for_config, parse_file
from nirjas.languages.tree_sitter.comment_span import CommentSpan


class LanguageRegistryTest(unittest.TestCase):
    def test_nirjas_name_from_path(self):
        self.assertEqual(nirjas_name_from_path("foo.py"), "python")
        self.assertEqual(nirjas_name_from_path("bar.cpp"), "cpp")

    def test_unsupported_extension_raises(self):
        with self.assertRaises(NotSupportedExtension):
            nirjas_name_from_path("file.xyz")

    def test_parser_name_aliases(self):
        self.assertEqual(parser_name("c_sharp"), "csharp")
        self.assertEqual(parser_name("shell"), "bash")
        self.assertEqual(parser_name("python"), "python")

    def test_parser_name_for_tsx(self):
        self.assertEqual(parser_name_for_path("component.tsx"), "tsx")
        self.assertEqual(parser_name_for_path("module.ts"), "typescript")


class LanguageConfigTest(unittest.TestCase):
    def test_frozen_config_fields(self):
        config = LanguageConfig(
            display_language="C",
            parser_language="c",
            comment_node_kinds=frozenset({"comment"}),
            single_line_prefixes=("//",),
            multi_line_delimiters=(("/*", "*/"),),
        )
        self.assertEqual(config.display_language, "C")
        self.assertEqual(config.comment_node_kinds, frozenset({"comment"}))

    def test_config_extension_parser_override(self):
        ts_parser = get_cached_parser_for_config(
            typescript.TYPESCRIPT_CONFIG,
            "component.ts",
        )
        tsx_parser = get_cached_parser_for_config(
            typescript.TYPESCRIPT_CONFIG,
            "component.tsx",
        )

        self.assertIsNot(ts_parser, tsx_parser)


class CommentSpanTest(unittest.TestCase):
    def test_comment_span_is_frozen(self):
        span = CommentSpan(
            start_byte=0,
            end_byte=10,
            start_line=1,
            end_line=1,
            node_kind="comment",
            is_documentation=False,
            raw_text="# hello",
        )
        with self.assertRaises(AttributeError):
            span.start_byte = 5  # type: ignore[misc]


class LanguageHandlerTest(unittest.TestCase):
    def test_default_handler_returns_none(self):
        handler = DefaultHandler()
        self.assertIsNone(handler.is_documentation_comment(None, None, ""))

    def test_get_handler_fallback(self):
        self.assertIsInstance(get_handler(None), DefaultHandler)
        self.assertIsInstance(get_handler("unknown"), DefaultHandler)
        self.assertIsInstance(get_handler("python"), PythonHandler)

    def test_python_handler_docstring_under_module(self):
        source = '"""module doc"""\nx = 1\n'
        handler = PythonHandler()
        string_node, parent = _require_string_node(source)
        self.assertTrue(handler.is_documentation_comment(string_node, parent, source))

    def test_python_handler_string_literal_not_docstring(self):
        source = 'x = """not a doc"""\n'
        handler = PythonHandler()
        string_node, parent = _require_string_node(source)
        self.assertFalse(handler.is_documentation_comment(string_node, parent, source))

    def test_python_handler_skips_leading_comments(self):
        source = '# leading\n"""real doc"""\n'
        handler = PythonHandler()
        string_node, parent = _require_string_node(source)
        self.assertTrue(handler.is_documentation_comment(string_node, parent, source))


class CommentAccountingTest(unittest.TestCase):
    """Metadata arithmetic: comment lines, blank lines and their overlap."""

    def test_blank_line_inside_block_comment_counts_as_blank(self):
        """A blank line stays blank even when a comment block surrounds it."""

        source = "/* header\n\n   still header */\nint x = 1;\n"
        metadata = _scan(source, ".c", c.cExtractor)["metadata"]

        self.assertEqual(metadata["total_lines"], 4)
        self.assertEqual(metadata["blank_lines"], 1)
        self.assertEqual(metadata["total_lines_of_comments"], 2)
        self.assertEqual(metadata["sloc"], 1)

    def test_code_with_trailing_comment_counts_as_code(self):
        """A line carrying both code and a comment belongs to `sloc`."""

        source = "int x = 1; /* set x */\nint y = 2; // set y\n/* pure */\n"
        metadata = _scan(source, ".c", c.cExtractor)["metadata"]

        self.assertEqual(metadata["total_lines"], 3)
        self.assertEqual(metadata["blank_lines"], 0)
        self.assertEqual(metadata["total_lines_of_comments"], 1)
        self.assertEqual(metadata["sloc"], 2)

    def test_buckets_account_for_every_line_once(self):
        """blank + comment + sloc must reconstruct the line total."""

        source = (
            "/* header\n\n   still header */\n"
            "int x = 1; // trailing\n"
            "\n"
            "// standalone\n"
            "int y = 2;\n"
        )
        metadata = _scan(source, ".c", c.cExtractor)["metadata"]

        bucket_total = metadata["total_lines_of_comments"] + metadata["blank_lines"] + metadata["sloc"]

        self.assertEqual(bucket_total, metadata["total_lines"])
        self.assertEqual(metadata["total_lines"], 7)
        self.assertEqual(metadata["blank_lines"], 2)
        self.assertEqual(metadata["total_lines_of_comments"], 3)
        self.assertEqual(metadata["sloc"], 2)

    def test_block_closing_before_code_counts_as_code(self):
        """Code after a block terminator keeps the line in `sloc`.

        `cloc` calls this line a comment, which understates `sloc` because the
        line holds a statement. It documents mixed lines as code and tracks the
        mismatch as a defect (AlDanial/cloc#875), and `scc` counts it as code,
        so the divergence from `cloc` here is intentional.
        """

        source = "int a = 1; /* opens\n   inside\n*/ int b = 2;\n"
        metadata = _scan(source, ".c", c.cExtractor)["metadata"]

        self.assertEqual(metadata["total_lines"], 3)
        self.assertEqual(metadata["blank_lines"], 0)
        self.assertEqual(metadata["total_lines_of_comments"], 1)
        self.assertEqual(metadata["sloc"], 2)

    def test_shebang_counts_as_code(self):
        """A shebang directs the OS, so it is code rather than a comment."""

        source = "#!/bin/bash\n# real comment\necho hi\n"
        metadata = _scan(source, ".sh", shell.shellExtractor)["metadata"]

        self.assertEqual(metadata["total_lines"], 3)
        self.assertEqual(metadata["total_lines_of_comments"], 1)
        self.assertEqual(metadata["sloc"], 2)

    def test_hash_comment_after_first_line_is_not_a_shebang(self):
        """Only line 1 gets the shebang treatment."""

        source = "echo hi\n#!not a shebang\n"
        metadata = _scan(source, ".sh", shell.shellExtractor)["metadata"]

        self.assertEqual(metadata["total_lines_of_comments"], 1)
        self.assertEqual(metadata["sloc"], 1)

    def test_comment_token_in_string_is_code_not_comment(self):
        """The false positive this migration exists to remove.

        `cloc` reads these two lines as comments because it matches comment
        tokens with regexes. `tokei`, `scc` and Nirjas all read them as code.
        """

        source = 'a = "/*"\nb = "*/"\nc = 1\n'
        metadata = _scan(source, ".py", python.pythonExtractor)["metadata"]

        self.assertEqual(metadata["total_lines_of_comments"], 0)
        self.assertEqual(metadata["sloc"], 3)

    def test_byte_order_mark_is_not_code(self):
        """A leading BOM is encoding metadata, not code on line 1."""

        source = "\ufeff/* header */\nint x = 1;\n"
        metadata = _scan(source, ".c", c.cExtractor)["metadata"]

        self.assertEqual(metadata["total_lines"], 2)
        self.assertEqual(metadata["total_lines_of_comments"], 1)
        self.assertEqual(metadata["sloc"], 1)

    def test_multiline_comment_node_kind_is_not_single_line(self):
        """`multiline_comment` contains `line_comment` as a substring."""

        source = 'fun main() {\n    /* one\n       two */\n    println("hi")\n}\n'
        scan_output = _scan(source, ".kts", kotlin.kotlinExtractor)

        self.assertEqual(scan_output["single_line_comment"], [])
        self.assertEqual(len(scan_output["multi_line_comment"]), 1)
        self.assertEqual(scan_output["multi_line_comment"][0]["start_line"], 2)
        self.assertEqual(scan_output["multi_line_comment"][0]["end_line"], 3)
        self.assertEqual(scan_output["metadata"]["total_lines_of_comments"], 2)


def _scan(source: str, suffix: str, extractor) -> dict:
    with tempfile.TemporaryDirectory() as temp_dir:
        source_file = os.path.join(temp_dir, "sample" + suffix)
        with open(source_file, "w", encoding="utf-8") as handle:
            handle.write(source)
        return extractor(source_file).get_dict()


def _python_parser():
    from nirjas.languages.parser_cache import get_cached_parser

    return get_cached_parser("python")


def _require_string_node(source: str) -> tuple[Any, Any]:
    tree, _ = parse_file(_python_parser(), source)
    root = tree.root_node
    found = _find_node(root, "string")
    if found is None:
        raise AssertionError("expected a string node in parse tree")
    return found


def _find_node(root: Any, kind: str) -> tuple[Any, Any] | None:
    if root.type == kind:
        return root, root.parent

    for index in range(root.child_count):
        found = _find_node(root.child(index), kind)
        if found is not None:
            return found
    return None


if __name__ == "__main__":
    unittest.main()
