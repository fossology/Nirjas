#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for Tree-Sitter based comment parsing.

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

import importlib
import os
import tempfile
import unittest


class TreeSitterRegressionTest(unittest.TestCase):
    """Ensure string literals are not misidentified as comments."""

    CASES = [
        (
            "python",
            ".py",
            'value = "# not a comment"\n# real comment\n',
            "real comment",
        ),
        (
            "r",
            ".R",
            'value <- "# not a comment"\n# real comment\n',
            "real comment",
        ),
        (
            "perl",
            ".pl",
            'my $value = "# not a comment";\n# real comment\n',
            "real comment",
        ),
        (
            "shell",
            ".sh",
            'value="# not a comment"\n# real comment\n',
            "real comment",
        ),
        (
            "javascript",
            ".js",
            (
                'const url = "https://example.com/path";\n'
                'const marker = "// not a comment";\n'
                "// real comment\n"
            ),
            "real comment",
        ),
        (
            "typescript",
            ".ts",
            'const marker = "// not a comment";\n// real comment\n',
            "real comment",
        ),
        (
            "java",
            ".java",
            'class T { String marker = "// not a comment"; }\n// real comment\n',
            "real comment",
        ),
        (
            "c",
            ".c",
            (
                'const char *a = "/* not a comment */";\n'
                'const char *b = "// not a comment";\n'
                "// line comment\n"
                "/* block comment */\n"
            ),
            "line comment",
        ),
        (
            "css",
            ".css",
            'a::before { content: "/* not a comment */"; }\n/* real comment */\n',
            "real comment",
        ),
        (
            "html",
            ".html",
            '<script>const x = "<!-- not a comment -->";</script>\n<!-- real comment -->\n',
            "real comment",
        ),
        (
            "sql",
            ".sql",
            "SELECT '-- not a comment';\n-- real comment\n",
            "real comment",
        ),
        (
            "haskell",
            ".hs",
            'value = "-- not a comment"\n-- real comment\n',
            "real comment",
        ),
    ]

    SOURCE_STRIP_CASES = [
        (
            "python",
            ".py",
            'value = "# not a comment"\n# real comment\nprint(value)\n',
            ['value = "# not a comment"', "print(value)"],
            ["real comment"],
        ),
        (
            "javascript",
            ".js",
            (
                'const marker = "// not a comment";\n'
                "// real comment\n"
                "console.log(marker);\n"
            ),
            ['const marker = "// not a comment";', "console.log(marker);"],
            ["real comment"],
        ),
        (
            "c",
            ".c",
            (
                'const char *marker = "/* not a comment */";\n'
                "/* real block comment */\n"
                "int main(void) { return 0; }\n"
            ),
            [
                'const char *marker = "/* not a comment */";',
                "int main(void) { return 0; }",
            ],
            ["real block comment"],
        ),
        (
            "html",
            ".html",
            (
                '<script>const marker = "<!-- not a comment -->";</script>\n'
                "<!-- real html comment -->\n"
                "<div>content</div>\n"
            ),
            [
                '<script>const marker = "<!-- not a comment -->";</script>',
                "<div>content</div>",
            ],
            ["real html comment"],
        ),
        (
            "sql",
            ".sql",
            "SELECT '-- not a comment';\n-- real sql comment\nSELECT 1;\n",
            ["SELECT '-- not a comment';", "SELECT 1;"],
            ["real sql comment"],
        ),
        (
            "typescript",
            ".tsx",
            (
                'const marker = "// not a comment";\n'
                "// real tsx comment\n"
                "const view = <div>{marker}</div>;\n"
            ),
            [
                'const marker = "// not a comment";',
                "const view = <div>{marker}</div>;",
            ],
            ["real tsx comment"],
        ),
    ]

    def _extract_with_temp_file(self, suffix: str, content: str, extractor):
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=suffix,
            delete=False,
            encoding="utf-8",
        ) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        try:
            return extractor(temp_path).get_dict()
        finally:
            os.unlink(temp_path)

    def _strip_with_temp_file(self, suffix: str, content: str, source_extractor):
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=suffix,
            delete=False,
            encoding="utf-8",
        ) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        output_path = temp_path + ".out"
        try:
            returned_path = source_extractor(temp_path, output_path)
            self.assertEqual(returned_path, output_path)
            with open(output_path, encoding="utf-8") as stripped_file:
                return stripped_file.read()
        finally:
            os.unlink(temp_path)
            if os.path.exists(output_path):
                os.unlink(output_path)

    @staticmethod
    def _all_comment_texts(scan_output: dict) -> list[str]:
        comments = [
            entry["comment"] for entry in scan_output["single_line_comment"]
        ]
        comments.extend(
            entry["comment"] for entry in scan_output["cont_single_line_comment"]
        )
        comments.extend(
            entry["comment"] for entry in scan_output["multi_line_comment"]
        )
        return comments

    def test_comment_tokens_inside_strings_are_not_comments(self):
        for module_name, suffix, content, expected_comment in self.CASES:
            with self.subTest(language=module_name):
                module = importlib.import_module(f"nirjas.languages.{module_name}")
                extractor = getattr(module, f"{module_name}Extractor")
                scan_output = self._extract_with_temp_file(
                    suffix=suffix,
                    content=content,
                    extractor=extractor,
                )

                comment_texts = self._all_comment_texts(scan_output)
                self.assertIn(expected_comment, comment_texts)
                self.assertFalse(any("not a comment" in text for text in comment_texts))

    def test_source_stripping_preserves_strings_and_removes_comments(self):
        for (
            module_name,
            suffix,
            content,
            expected_fragments,
            removed_fragments,
        ) in self.SOURCE_STRIP_CASES:
            with self.subTest(language=module_name, suffix=suffix):
                module = importlib.import_module(f"nirjas.languages.{module_name}")
                source_extractor = getattr(module, f"{module_name}Source")
                stripped_source = self._strip_with_temp_file(
                    suffix,
                    content,
                    source_extractor,
                )

                for expected_fragment in expected_fragments:
                    self.assertIn(expected_fragment, stripped_source)

                for removed_fragment in removed_fragments:
                    self.assertNotIn(removed_fragment, stripped_source)

    def test_grammar_specific_line_comment_kinds_are_detected(self):
        """Some grammars give `//` and `--` comments a non-obvious node kind.

        SCSS reports `//` as `js_comment` and SQL reports `--` as `marginalia`.
        Leaving either out of the config drops every single-line comment in the
        file while still parsing cleanly, so the loss is silent.
        """

        cases = [
            ("scss", ".scss", "// line one\n// line two\n.a { color: red; }\n"),
            ("sql", ".sql", "-- line one\n-- line two\nSELECT 1;\n"),
        ]

        for module_name, suffix, content in cases:
            with self.subTest(language=module_name):
                module = importlib.import_module(f"nirjas.languages.{module_name}")
                extractor = getattr(module, f"{module_name}Extractor")
                scan_output = self._extract_with_temp_file(
                    suffix=suffix,
                    content=content,
                    extractor=extractor,
                )

                comment_texts = self._all_comment_texts(scan_output)
                self.assertTrue(any("line one" in text for text in comment_texts))
                self.assertTrue(any("line two" in text for text in comment_texts))
                self.assertEqual(
                    scan_output["metadata"]["total_lines_of_comments"],
                    2,
                )
                self.assertEqual(scan_output["metadata"]["sloc"], 1)
