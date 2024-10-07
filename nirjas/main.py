#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (C) 2020  Ayush Bhardwaj (classicayush@gmail.com),
Kaushlendra Pratap (kaushlendrapratap.9837@gmail.com)

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

import argparse
import json
import os

from nirjas.languages import *  # noqa


class NotSupportedExtension(Exception):
    """
    Exception if file extension is not recognized
    """

    def __str__(self):
        return "extension '" + self.args[0] + "' not supported"


class LanguageMapper:
    """
    Class to help identify language based on file extension
    """

    LANG_MAP = {
        ".py": "python",
        ".m4": "python",
        ".nsi": "python",
        ".hpp": "cpp",
        ".c": "c",
        ".h": "cpp",
        ".cs": "c_sharp",
        ".cpp": "cpp",
        ".scss": "scss",
        ".sep": "cpp",
        ".hxx": "cpp",
        ".cc": "cpp",
        ".css": "css",
        ".dart": "dart",
        ".go": "go",
        ".hs": "haskell",
        ".html": "html",
        ".xml": "html",
        ".java": "java",
        ".js": "javascript",
        ".jsx": "javascript",
        ".jl": "julia",
        ".kt": "kotlin",
        ".kts": "kotlin",
        ".ktm": "kotlin",
        ".m": "matlab",
        ".php": "php",
        ".pl": "perl",
        ".r": "r",
        ".R": "r",
        ".rb": "ruby",
        ".rs": "rust",
        ".sh": "shell",
        ".sql": "sql",
        ".swift": "swift",
        ".scala": "scala",
        ".sc": "scala",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".txt": "text",
        ".lic": "text",
        ".install": "text",
        ".OSS": "text",
        ".gl": "text",
    }

    @staticmethod
    def langIdentifier(file):
        """
        Return the programming language based on extension of path passed.
        """
        extension = os.path.splitext(file)[1]
        if extension not in LanguageMapper.LANG_MAP:
            raise NotSupportedExtension(extension)
        return LanguageMapper.LANG_MAP[extension]


def run_and_print():
    """
    Call the run_cli() method and print results to stdout.
    """
    print(run_cli())


def run_cli():
    """
    Accept the parameters from CLI,
    run the nirjas logic and return the results.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        default=None,
        nargs="?",
        help="Specify the input file/directory path to scan",
    )
    parser.add_argument(
        "-i",
        "--inputFile",
        default=None,
        help="Specify the input file to extract the source code from",
    )
    parser.add_argument(
        "-o",
        "--outFile",
        help="The name of file to put the code in",
        default="source.txt",
    )
    args = parser.parse_args()
    file = args.path
    inputfile = args.inputFile
    out_file = args.outFile
    try:
        if file is not None:
            return file_runner(file, "json")
        return inputfile_runner(inputfile, out_file)
    except NotSupportedExtension as e:
        print(e, file=os.sys.stderr)
        return None


def scan_the_file(file):
    """
    Run scanner on single file and return the results.
    :param file: File to scan
    :type file: string
    :return: Scan result
    :rtype: ScanOutput
    """
    langname = LanguageMapper.langIdentifier(file)
    func = langname + "." + langname + "Extractor"

    return eval(func)(file)


def file_runner(file, type="dictionary"):
    """
    Check if the input is a file or a directory and iterate with
    scan_the_file()
    :param file: Path to scan
    :type file: string
    :return: List of scan result
    :rtype: list
    """
    result = []
    if os.path.isfile(file):
        result = scan_the_file(file).get_dict()
    elif os.path.isdir(file):
        for root, _, files in os.walk(file, followlinks=True):
            for scanfile in files:
                file_to_scan = os.path.join(root, scanfile)
                try:
                    if os.path.isfile(file_to_scan):
                        result.append(scan_the_file(file_to_scan).get_dict())
                except Exception:
                    continue
    if type == "json":
        return json.dumps(result, sort_keys=False, indent=4)
    return result


def inputfile_runner(inputfile, out_file):
    """
    Extract the source from inputfile and put at out_file.
    :param inputfile: File to process
    :type inputfile: string
    :param out_file: Output file location
    :type out_file: string
    """
    langname = LanguageMapper.langIdentifier(inputfile)
    func = langname + "." + langname + "Source"
    return eval(func)(inputfile, out_file)


if __name__ == "__main__":
    run_and_print()
