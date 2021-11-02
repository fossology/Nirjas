#!/usr/bin/env python3

"""
nirjas module which can be imported by other tools

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

from nirjas.main import file_runner  # noqa


def extract(file):
    """
    Extract the information from the given file.
    :param file: File or directory to get information from
    :type file: string
    :return: Returns comments and other meta information about the given file.
    """
    return file_runner(file)  # noqa


__all__ = ["file_runner", "extract", "LanguageMapper"]
