#!/usr/bin/env python3
"""
Download Tree-Sitter parser bundles required by Nirjas.

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

Usage:
    python3 scripts/download_parsers.py
    python3 scripts/download_parsers.py --config language-pack.toml
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

from nirjas.language_registry import parser_name
from tree_sitter_language_pack import download

try:
    import tomllib  # pyright: ignore[reportMissingImports]
except ImportError:  # pragma: no cover - Python 3.10 fallback
    tomllib = None


class ParserDownloadError(Exception):
    """Raised when parser download config is invalid or download fails."""


def parse_language_config(config_path: Path) -> list[str]:
    """Parse configured parser names from language-pack.toml."""

    if not config_path.exists():
        raise ParserDownloadError(f"Config file not found: {config_path}")

    if tomllib is None:
        config = _parse_minimal_toml(config_path)
    else:
        with config_path.open("rb") as config_file:
            config = tomllib.load(config_file)

    raw_languages = config.get("languages")
    if not isinstance(raw_languages, list):
        raise ParserDownloadError(
            f"Could not find `languages = [ ... ]` list in config: {config_path}"
        )

    languages = [
        language_name.strip()
        for language_name in raw_languages
        if isinstance(language_name, str) and language_name.strip()
    ]

    if not languages:
        raise ParserDownloadError(f"No languages configured in: {config_path}")

    return languages


def _parse_minimal_toml(config_path: Path) -> dict[str, object]:
    """Parse the simple top-level TOML list used by Python 3.10 CI."""

    lines = config_path.read_text(encoding="utf-8").splitlines()
    collecting = False
    list_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not collecting and stripped.startswith("languages"):
            _, _, remainder = stripped.partition("=")
            list_lines.append(remainder.strip())
            collecting = True
        elif collecting:
            list_lines.append(stripped)

        if collecting and "]" in stripped:
            break

    if not list_lines:
        return {}

    try:
        return {"languages": ast.literal_eval("\n".join(list_lines))}
    except (SyntaxError, ValueError) as exc:
        raise ParserDownloadError(
            f"Could not parse `languages` list in config: {config_path}"
        ) from exc


def normalize_language_names(language_names: list[str]) -> list[str]:
    """Normalize aliases and deduplicate while preserving order."""

    normalized_names: list[str] = []
    seen_languages: set[str] = set()

    for language_name in language_names:
        normalized_name = parser_name(language_name)
        if normalized_name in seen_languages:
            continue
        normalized_names.append(normalized_name)
        seen_languages.add(normalized_name)

    return normalized_names


def download_parsers(config_path: Path) -> int:
    """Download parser bundles from config file and return count."""

    configured_language_names = parse_language_config(config_path)
    language_names = normalize_language_names(configured_language_names)

    try:
        downloaded = download(language_names)
    except Exception as exc:  # pragma: no cover - depends on network/runtime
        raise ParserDownloadError(
            "Failed to download Tree-Sitter parsers. "
            f"Configured: {configured_language_names}. "
            f"Normalized: {language_names}. Error: {exc}"
        ) from exc

    return downloaded


def main() -> int:
    """CLI entrypoint."""

    parser = argparse.ArgumentParser(
        description="Download Tree-Sitter language parsers required by Nirjas",
    )
    parser.add_argument(
        "--config",
        default="language-pack.toml",
        help="Path to parser configuration file (default: language-pack.toml)",
    )
    args = parser.parse_args()

    config_path = Path(args.config)

    try:
        downloaded_count = download_parsers(config_path)
    except ParserDownloadError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(
        "Tree-Sitter parser download complete. "
        f"Downloaded/verified parsers: {downloaded_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
