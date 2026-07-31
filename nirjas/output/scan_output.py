#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (C) 2020 Siemens AG
Author: Gaurav Mishra <mishra.gaurav@siemens.com>
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

from .multi_line import MultiLine
from .single_line import SingleLine


class ScanOutput:
    """
    Generate the output for a single file scan.
    """

    def __init__(self) -> None:
        self.filename = ""
        self.lang = ""
        self.total_lines = 0
        self.total_lines_of_comments = 0
        self.blank_lines = 0
        self.single_line_comment: list[SingleLine] = []
        self.cont_single_line_comment: list[MultiLine] = []
        self.multi_line_comment: list[MultiLine] = []

    def get_dict(self) -> dict[str, object]:
        """
        Get the output as dictionary
        """
        # Every line belongs to exactly one bucket, so what is left after the
        # comment and blank lines are removed is the code.
        sloc = self.total_lines - self.total_lines_of_comments - self.blank_lines
        return {
            "metadata": {
                "filename": self.filename,
                "lang": self.lang,
                "total_lines": self.total_lines,
                "total_lines_of_comments": self.total_lines_of_comments,
                "blank_lines": self.blank_lines,
                "sloc": sloc,
            },
            "single_line_comment": [
                comment.get_dict() for comment in self.single_line_comment
            ],
            "cont_single_line_comment": [
                comment.get_dict() for comment in self.cont_single_line_comment
            ],
            "multi_line_comment": [
                comment.get_dict() for comment in self.multi_line_comment
            ],
        }
