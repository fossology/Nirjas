#!/usr/bin/env python3
"""
Download tree-sitter parsers listed in language-pack.toml.

Run after `uv sync`:
    uv run download-parsers
"""

import sys
import tomllib
from pathlib import Path


def main() -> None:
    config_path = Path(__file__).parent.parent / "language-pack.toml"
    if not config_path.exists():
        print(f"language-pack.toml not found at {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    languages = config.get("pack", {}).get("languages", [])
    if not languages:
        print("No languages configured in language-pack.toml")
        return

    from tree_sitter_language_pack import download, downloaded_languages

    already = set(downloaded_languages())
    needed = [lang for lang in languages if lang not in already]

    if not needed:
        print(f"All parsers already downloaded: {', '.join(languages)}")
        return

    print(f"Downloading parsers: {', '.join(needed)}")
    count = download(needed)
    print(f"Downloaded {count} parser(s).")


if __name__ == "__main__":
    main()
