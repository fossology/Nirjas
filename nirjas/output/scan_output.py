#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (C) 2020 Siemens AG
Author: Gaurav Mishra <mishra.gaurav@siemens.com>

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

from .output import Output


class ScanOutput:
    """
    Generate the output for a single file scan.
    """

    def __init__(self):
        self.filename = None
        self.lang = None
        self.total_lines = None
        self.total_lines_of_comments = None
        self.blank_lines = None
        self.single_line_comment = []
        self.cont_single_line_comment = []
        self.multi_line_comment = []

    def get_dict(self):
        """
        Get the output as dictionary
        """
        return Output(
            metadata=Output(
                filename=self.filename,
                lang=self.lang,
                total_lines=self.total_lines,
                total_lines_of_comments=self.total_lines_of_comments,
                blank_lines=self.blank_lines,
                sloc=self.total_lines
                - (self.total_lines_of_comments + self.blank_lines),
            ).output,
            single_line_comment=[c.get_dict() for c in self.single_line_comment],
            cont_single_line_comment=[
                c.get_dict() for c in self.cont_single_line_comment
            ],
            multi_line_comment=[c.get_dict() for c in self.multi_line_comment],
        ).output
