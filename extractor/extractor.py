#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse


class CommentExtractor:
    def __init__(self):
        pass

    def langIdentifier(self, file):
        extension = os.path.splitext(file)[1]
        
        
        langMap = {
            '.py': 'python',
            '.c': 'c',
            '.cs': 'c#',
            '.cpp': 'c++',
            '.css': 'css',
            '.go': 'go',
            '.hs': 'haskell',
            '.html': 'html',
            '.java': 'java',
            '.js': 'javascript',
            '.kt': 'kotlin',
            '.kts': 'kotlin',
            '.ktm': 'kotlin',
            '.m': 'matlab',
            '.php': 'php',
            '.pl': 'perl',
            '.r': 'r',
            '.rbb': 'ruby',
            '.rs': 'rust',
            '.sh': 'shell',
            '.swift': 'swift',
            '.scala': 'scala',
            '.sc': 'scala',
        }
        
        return langMap[extension]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help="Specify the input file path to scan")

    args = parser.parse_args()
    file = args.inputFile