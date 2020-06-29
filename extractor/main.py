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
    parser.add_argument("path", help="Specify the input file path to scan")

    args = parser.parse_args()
    file_path = args.path

    if os.path.basename(file_path):
        file_name = os.path.basename(file_path)
        current_path = os.getcwd()+'/'+file_path
        CommentExtractor.langIdentifier(file_name) 
        output = python.pythonExtractor(file_name,current_path)
        output = json.dumps(output, sort_keys=True, ensure_ascii=False, indent=4)
        print(output)
        
    
    elif  os.path.dirname(file_path):
        directory_name = os.path.dirname(file_path)
        for file_name in os.listdir(directory_name):
            current_path = os.getcwd()+'/'+file_path + '/'+ file_name
            CommentExtractor.langIdentifier(file_name)
            output = python.pythonExtractor(file_name,current_path)
            output = json.dumps(output, sort_keys=True, ensure_ascii=False, indent=4)
            print(output)
    

    
    # output = python.pythonExtractor(file_name,current_path)
    # output = json.dumps(output, sort_keys=True, ensure_ascii=False, indent=4)
    # print(output)


#    def traverse_dir(self,file_path):
#         if os.path.basename(file_path):
#             file = os.path.basename(file_path)
#             current_path = os.getcwd()+'/'+file_path
#             CommentExtractor.langIdentifier(self,current_path,file)
        
#         else:
#             directory_name = os.path.dirname(file_path)
#             for file in os.listdir(directory_name):
#                 current_path = os.getcwd()+'/'+file_path + '/'+ file
#                 CommentExtractor.langIdentifier(self,current_path, file)