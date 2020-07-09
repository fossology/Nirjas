#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2020  Ayush Bhardwaj (classicayush@gmail.com), Kaushlendra Pratap (kaushlendrapratap.9837@gmail.com)

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

import os
import json
import argparse

from binder import *
from languages import *


class CommentExtractor:
    def __init__(self):
        pass

    def langIdentifier(file):
        extension = os.path.splitext(file)[1]
        
        
        langMap = {
            '.py': 'python',
            '.c': 'c',
            '.cs': 'c#',
            '.cpp': 'c++',
            '.cc': 'c++',
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
            '.rb': 'ruby',
            '.rs': 'rust',
            '.sh': 'shell',
            '.swift': 'swift',
            '.scala': 'scala',
            '.sc': 'scala',
            '.pyc':'byte_code'
        }

        return langMap[extension]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--path", help="Specify the input file/directory path to scan")
    parser.add_argument("-i","--inputFile", help="Specify the input file with the source code")
    parser.add_argument("-s","--string",help= "The name of file you want the code in",default="source.txt")
    args = parser.parse_args()
    file = args.path
    inputfile = args.inputFile
    string_name = args.string
    result = []
    
    
    if file:
        if os.path.basename(file):
            file_name = os.path.basename(file)
            current_path = os.getcwd()+'/'+file
            langname = CommentExtractor.langIdentifier(file_name) 
            func = langname+'.'+langname+'Extractor'
            output = eval(func)(current_path)
            result.append(output)

        elif  os.path.dirname(file):
            for root,dirs,files in os.walk(file,topdown=True):
                for file in files:
                    current_path = os.path.join(os.path.join(os.getcwd(),root),file)
                    try:

                        if os.path.isfile(current_path):
                            langname = CommentExtractor.langIdentifier(file)
                            func = langname+'.'+langname+'Extractor'
                            output = eval(func)(current_path)
                            result.append(output)
                    except Exception:
                        continue

    elif inputfile:
        langname = CommentExtractor.langIdentifier(inputfile)
        func = langname+'.'+langname+'Source'
        eval(func)(inputfile,string_name)
        # python.pythonSource(inputfile,string_name)
    
    result = json.dumps(result, sort_keys=True, ensure_ascii=False, indent=4)
    print(result)   



if __name__ == "__main__":
    main()