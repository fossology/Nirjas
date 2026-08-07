#!/usr/bin/env python3
# a genuine single-line comment
"""Module docstring with a # inside ordinary prose."""

URL = "https://example.invalid/#fragment"
PATTERN = "# not a comment, just a string"
CONTINUED = "trailing hash # \
still inside the string"


def add(x, y):
    # a real comment inside a function
    return x + y  # trailing comment after code
