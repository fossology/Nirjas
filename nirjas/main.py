#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
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
"""

import os
import json
import argparse
import sys

from nirjas.language_registry import (
    EXTENSION_MAP,
    NotSupportedExtension,
    nirjas_name_from_path,
)
from nirjas.languages import (
    c,
    c_sharp,
    cpp,
    css,
    dart,
    go,
    haskell,
    html,
    java,
    javascript,
    julia,
    kotlin,
    matlab,
    perl,
    php,
    python,
    r,
    ruby,
    rust,
    scala,
    scss,
    shell,
    sql,
    swift,
    text,
    typescript,
)


class LanguageMapper:
    """Compatibility wrapper around the shared language registry."""

    LANG_MAP = EXTENSION_MAP

    @staticmethod
    def langIdentifier(file):
        """
        Return the programming language based on extension of path passed.
        """
        return nirjas_name_from_path(file)


EXTRACTORS = {
    "c": c.cExtractor,
    "c_sharp": c_sharp.c_sharpExtractor,
    "cpp": cpp.cppExtractor,
    "css": css.cssExtractor,
    "dart": dart.dartExtractor,
    "go": go.goExtractor,
    "haskell": haskell.haskellExtractor,
    "html": html.htmlExtractor,
    "java": java.javaExtractor,
    "javascript": javascript.javascriptExtractor,
    "julia": julia.juliaExtractor,
    "kotlin": kotlin.kotlinExtractor,
    "matlab": matlab.matlabExtractor,
    "perl": perl.perlExtractor,
    "php": php.phpExtractor,
    "python": python.pythonExtractor,
    "r": r.rExtractor,
    "ruby": ruby.rubyExtractor,
    "rust": rust.rustExtractor,
    "scala": scala.scalaExtractor,
    "scss": scss.scssExtractor,
    "shell": shell.shellExtractor,
    "sql": sql.sqlExtractor,
    "swift": swift.swiftExtractor,
    "text": text.textExtractor,
    "typescript": typescript.typescriptExtractor,
}

SOURCES = {
    "c": c.cSource,
    "c_sharp": c_sharp.c_sharpSource,
    "cpp": cpp.cppSource,
    "css": css.cssSource,
    "dart": dart.dartSource,
    "go": go.goSource,
    "haskell": haskell.haskellSource,
    "html": html.htmlSource,
    "java": java.javaSource,
    "javascript": javascript.javascriptSource,
    "julia": julia.juliaSource,
    "kotlin": kotlin.kotlinSource,
    "matlab": matlab.matlabSource,
    "perl": perl.perlSource,
    "php": php.phpSource,
    "python": python.pythonSource,
    "r": r.rSource,
    "ruby": ruby.rubySource,
    "rust": rust.rustSource,
    "scala": scala.scalaSource,
    "scss": scss.scssSource,
    "shell": shell.shellSource,
    "sql": sql.sqlSource,
    "swift": swift.swiftSource,
    "typescript": typescript.typescriptSource,
}


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
        print(e, file=sys.stderr)
        return None


def scan_the_file(file):
    """
    Run scanner on single file and return the results.
    :param file: File to scan
    :type file: string
    :return: Scan result
    :rtype: ScanOutput
    """
    langname = nirjas_name_from_path(file)
    return EXTRACTORS[langname](file)


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
    langname = nirjas_name_from_path(inputfile)
    return SOURCES[langname](inputfile, out_file)


if __name__ == "__main__":
    run_and_print()
