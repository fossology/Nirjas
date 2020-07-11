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

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
# fetch the long description from the README.md
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


CLASSIFIERS = """\
Development Status :: 4 - Beta
License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)
Programming Language :: Python :: 3 :: Only
Intended Audience :: Developers
Intended Audience :: Legal Industry
Topic :: Utilities
Topic :: Software Development
Topic :: Text Processing
"""


setup(
    name='Nirjas', 
    version='0.0.1',  
    description='A Python library to extract comments and source code out of your file(s)',  
    long_description=long_description,  
    long_description_content_type='text/markdown',  
    url='https://github.com/fossology/nirjas',  
    author='Ayush Bhardwaj, Kaushlendra Pratap',  
    author_email='classicayush@gmail.com, kaushlendrapratap.9837@gmail.com',  

    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
    keywords='Comment Extractor, Code Comment Extractor, Source Code Extractor, Source Extractor',  
    packages=find_packages(),  
    python_requires = ">=3",
    entry_points = {
    'console_scripts': [
      'nirjas = extractor.main:main'
    ]
  },
)