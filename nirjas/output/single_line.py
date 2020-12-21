#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
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
'''


class SingleLine(object):
    '''
    Store result for single line comments
    '''

    def __init__(self, line_number, comment):
        self.line_number = line_number
        self.comment = comment

    def get_dict(self):
        '''
        Get the output as dictionary
        '''
        return {
            "line_number": self.line_number,
            "comment": self.comment
        }
