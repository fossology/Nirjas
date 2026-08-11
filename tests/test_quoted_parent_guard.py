#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The quoted-parent guard, and what happens when it meets an unknown grammar.

`collect_comment_spans` drops a comment node whose immediate parent is a
quoting construct, because the delimiters there are data (issue #72). Two
questions follow from that, and this module answers both.

*Does it generalise?* Tree-Sitter has no cross-grammar notion of "this node is
quoted text" -- node kinds are named by each grammar author and nothing in the
API marks a rule as a string -- so the guard cannot ask the library. What it
can do is match the naming convention every grammar converges on, which is
`kind_looks_quoted`. `QUOTED_PARENT_NODE_KINDS` then names the kinds that have
actually been read in the grammar, and the tests below pin that the two agree:
the audited set buys silence, not a different answer.

*Does a gap stay visible?* A parent kind matched only by convention emits
`UnverifiedQuotedParentWarning`, which this suite escalates to an error via
`filterwarnings` in pyproject.toml. A grammar upgrade that renames a string
rule therefore fails the run rather than quietly resurrecting the bug.

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

from pathlib import Path

import pytest

from helpers import golden
from nirjas.language_registry import nirjas_name_from_path
from nirjas.languages.tree_sitter import comment_visitor
from nirjas.languages.tree_sitter.comment_visitor import QUOTED_PARENT_NODE_KINDS
from nirjas.languages.tree_sitter.comment_visitor import UnverifiedQuotedParentWarning
from nirjas.languages.tree_sitter.comment_visitor import kind_looks_quoted
from nirjas.main import EXTRACTORS

#: Node kinds naming a quoting construct, drawn from grammars Nirjas does not
#: currently ship a language for. They are here precisely because no audited set
#: could contain them: they stand in for the next grammar somebody adds.
QUOTED_KINDS_FROM_UNSHIPPED_GRAMMARS = (
    "interpreted_string_literal",  # tree-sitter-go
    "quoted_template",  # tree-sitter-hcl
    "quoted_content",  # tree-sitter-bash
    "heredoc_body",  # tree-sitter-bash
    "single_quoted_string",  # tree-sitter-nix
    "string_fragment",  # tree-sitter-json
    "unquoted_attribute_value",  # tree-sitter-vue
)

#: Kinds that hold *code* even though a string sits somewhere in their name.
#: Suppressing a comment under one of these would delete a real comment, which
#: is the failure mode that makes a name-based rule worth testing at all.
CODE_BEARING_KINDS = (
    "string_interpolation",  # tree-sitter-swift, tree-sitter-scala
    "template_substitution",  # tree-sitter-javascript
    "interpolation",  # tree-sitter-ruby
    "command_substitution",  # tree-sitter-bash
    "expansion",  # tree-sitter-bash
    "embedded_expression",  # tree-sitter-glimmer
    "source_file",
    "program",
    "block",
    "function_definition",
    "expression_statement",
    "argument_list",
)


@pytest.fixture(autouse=True)
def _forget_previous_reports():
    """The warning fires once per novel construct per process, by design."""

    comment_visitor.reset_unverified_quoted_parent_reports()
    yield
    comment_visitor.reset_unverified_quoted_parent_reports()


@pytest.mark.parametrize("node_kind", sorted(QUOTED_PARENT_NODE_KINDS))
def test_audited_kinds_also_match_the_convention(node_kind: str):
    """The audited set must be a subset of the rule, not a second opinion.

    If a kind needed to be listed *because* the convention misses it, the two
    mechanisms would disagree and an unshipped grammar using the same name
    would get the wrong answer. Keeping them aligned is what makes the set
    purely about silencing the warning.
    """

    assert kind_looks_quoted(node_kind), (
        f"'{node_kind}' is audited as quoted but does not match "
        "QUOTED_KIND_MARKERS; either the markers need widening or the kind "
        "needs a comment explaining why it is a genuine exception"
    )


@pytest.mark.parametrize("node_kind", QUOTED_KINDS_FROM_UNSHIPPED_GRAMMARS)
def test_convention_covers_grammars_we_do_not_ship(node_kind: str):
    assert kind_looks_quoted(node_kind)


@pytest.mark.parametrize("node_kind", CODE_BEARING_KINDS)
def test_convention_never_claims_a_code_bearing_kind(node_kind: str):
    assert not kind_looks_quoted(node_kind)


def test_interpolation_wins_over_a_string_in_the_same_name():
    """`string_interpolation` carries both markers; the hole must win.

    Swift and Scala both name the hole after its enclosing string. Without
    precedence the `string` marker would match and delete every comment written
    inside an interpolation.
    """

    assert not kind_looks_quoted("string_interpolation")
    assert kind_looks_quoted("string_literal")


def test_unaudited_quoted_parent_warns_and_still_suppresses(monkeypatch):
    """Strip the audited set: the convention alone must reach the same verdict.

    This is the evidence that `QUOTED_PARENT_NODE_KINDS` is documentation
    rather than the mechanism. tree-sitter-swift nests `multiline_comment`
    inside `line_string_literal`; with the set emptied that kind is unknown, so
    the guard falls back to the name, suppresses, and says it did so.
    """

    monkeypatch.setattr(comment_visitor, "QUOTED_PARENT_NODE_KINDS", frozenset())

    fixture = (
        golden.FIXTURE_ROOT / "swift" / "single_line_string_block_tokens.swift"
    )
    assert fixture.is_file(), "fixture pinning the Swift quoted-literal case is gone"

    with pytest.warns(UnverifiedQuotedParentWarning) as caught:
        scan_output: dict = EXTRACTORS["swift"](str(fixture)).get_dict()

    message = str(caught[0].message)
    assert "line_string_literal" in message
    assert "QUOTED_PARENT_NODE_KINDS" in message, (
        "the warning must name what to update, or it is just noise"
    )

    extracted = [entry["comment"] for entry in scan_output["single_line_comment"]]
    for section in ("cont_single_line_comment", "multi_line_comment"):
        extracted += [entry["comment"] for entry in scan_output[section]]
    assert not [text for text in extracted if "not a comment" in text], (
        "the fallback warned but let the false positive through anyway"
    )


def test_unaudited_report_is_emitted_once_per_construct(monkeypatch):
    """A scan over a large tree must not warn per node."""

    monkeypatch.setattr(comment_visitor, "QUOTED_PARENT_NODE_KINDS", frozenset())

    fixture = (
        golden.FIXTURE_ROOT / "swift" / "single_line_string_block_tokens.swift"
    )
    with pytest.warns(UnverifiedQuotedParentWarning) as caught:
        EXTRACTORS["swift"](str(fixture)).get_dict()
        EXTRACTORS["swift"](str(fixture)).get_dict()

    kinds = {str(warning.message).split("'")[3] for warning in caught}
    assert len(caught) == len(kinds), (
        f"{len(caught)} warnings for {len(kinds)} distinct constructs; "
        "deduplication is not holding"
    )


@pytest.mark.parametrize("fixture", golden.iter_fixtures(), ids=golden.fixture_id)
def test_shipped_grammars_need_no_fallback(fixture: Path):
    """Every quoting construct in the shipped grammars is audited.

    `filterwarnings` turns the warning into an error for the whole suite, so
    this passes only while the audited set is complete for what Nirjas ships.
    A grammar upgrade that renames a string rule fails here.
    """

    EXTRACTORS[nirjas_name_from_path(str(fixture))](str(fixture)).get_dict()
