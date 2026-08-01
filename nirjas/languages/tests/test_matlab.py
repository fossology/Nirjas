#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contract tests for MATLAB extractor.

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

import os
import unittest

from nirjas.languages import matlab
from nirjas.languages.tests._contract import (
    assert_scan_output_contract,
    assert_source_extractor_contract,
)


class MatlabTest(unittest.TestCase):
    """Contract tests for MATLAB language support."""

    testfile = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "TestFiles/textcomment.m",
    )

    def test_output_contract(self):
        """Verify extractor schema and metadata invariants."""

        scan_result = matlab.matlabExtractor(self.testfile).get_dict()
        assert_scan_output_contract(self, scan_result, self.testfile, 'MATLAB')

    def test_source_contract(self):
        """Verify source extraction API contract."""

        assert_source_extractor_contract(self, matlab.matlabSource, self.testfile)
