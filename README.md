# Nirjas

A Python library for Comments and Source Code Extraction

## Description

A source code file usually contains various vital information such as license text, function/class documentation, code/logic explanation, etc in the form of comments (block & line). 

Nirjas is a fully dedicated python library to extract the comments and source code out of your file(s). The extracted comments can be processed in various ways to detect licenses, generate documentation, process info, etc.

Apart from that the library serves you with all the required metdata about your Code, Comments and File(s)

## Requirements
- Python 3

Installing Python on Linux machines:

` $ sudo apt-get install python3 python3-pip `

For macOS and Windows, packages are available at [Python.org](https://www.python.org/downloads/)

## Supported Languages

We Support almost all the major programming languages. If you want any other language to be added, feel free to raise an issue.

The Languages we support till now:

- C
- C#
- C++
- CSS
- Go
- Haskell
- HTML
- Java
- JavaScript
- Kotlin
- MATLAB
- Perl
- PHP
- Python
- R
- Ruby
- Rust
- Scala
- Shell
- Swift

## Installation

### Install using source

You need to install Nirjas on your own system to try and test it out.
I recommend you to set up a separate Python virtual environment for the same.

> If you don't know how to set up a Python Virtual environment, please check out [Setting up a Python Virtual Environment](https://github.com/hastagAB/atarashi/wiki/Contribute-to-Atarashi#1-setting-up-a-python-virtual-environment)

* Fork the repo

* Clone on your local system

    `git clone https://github.com/fossology/Nirjas.git `

* Change directory

    `cd Nirjas/`

* Install the package

    `pip install .`

> This will install Nirjas on your system. 


* Check if Nirjas is installed correctly or get help, Run:

    `nirjas -h` or `nirjas --help`


## Example Usage

- For help

`nirjas -h`

- To extract comments from a single file

`nirjas -p <path to file>`

- To extract comments from all the files in directory/sub-directory

`nirjas -p <path to directory>`

- To extract only source code (excludes commented part) out of a file

`nirjas -i <target file> <new file name including extension>`

or for default file generation (default file: source.txt)

`nirjas -i <target file>`

## Contributing 

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

A detailed overview on how to contribute can be found in the [contributing guide](/CONTRIBUTING.md). 

Feel free to ask questions on [Slack](https://fossology.slack.com/)

## License
This repository is licensed under the terms of [LGPL-2.1](/LICENSE). Check the [LICENSE](/LICENSE) file for more details.