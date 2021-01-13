<h1 align="center">Nirjas ~ নির্যাস</h1>

<p align="center"><i>A Python library for Comments and Source Code Extraction</i></p>

<p align="center">✨ 🍰 ✨</p>

<p align="center">

![python version](https://img.shields.io/badge/Python-v3%2B-blue)
![Unit Tests](https://github.com/fossology/Nirjas/workflows/Unit%20Tests/badge.svg)
![status](https://img.shields.io/pypi/status/Nirjas)
[![HitCount](http://hits.dwyl.com/fossology/Nirjas.svg)](http://hits.dwyl.com/fossology/Nirjas)
![License LGPL-2.1](https://img.shields.io/github/license/fossology/nirjas)
![release](https://img.shields.io/github/v/release/fossology/Nirjas)
[![Slack Channel](https://img.shields.io/badge/slack-fossology-blue.svg?longCache=true&logo=slack)](https://join.slack.com/t/fossology/shared_invite/enQtNzI0OTEzMTk0MjYzLTYyZWQxNDc0N2JiZGU2YmI3YmI1NjE4NDVjOGYxMTVjNGY3Y2MzZmM1OGZmMWI5NTRjMzJlNjExZGU2N2I5NGY)
![stars](https://img.shields.io/github/stars/fossology/nirjas?style=social)

</p>

## Description

A source code file usually contains various vital information such as license text, function/class documentation, code/logic explanation, etc in the form of comments (block & line).

Nirjas is a fully dedicated python library to extract the comments and source code out of your file(s). The extracted comments can be processed in various ways to detect licenses, generate documentation, process info, etc.

Apart from that the library serves you with all the required metadata about your Code, Comments and File(s)

## Requirements
- Python 3

Installing Python on Linux machines:

```sh
$ sudo apt-get install python3 python3-pip
```

For macOS and Windows, packages are available at [Python.org](https://www.python.org/downloads/)

## Supported Languages

We Support almost all the major programming languages. If you want any other language to be added, feel free to raise an issue.

The Languages we support till now:

- C
- C#
- C++
- CSS
- Dart
- Go
- Haskell
- HTML
- Java
- JavaScript
- JSX
- Kotlin
- MATLAB
- Perl
- PHP
- Python
- R
- Ruby
- Rust
- Scala
- Scss
- Shell
- Swift
- TypeScript
- TSX

## Installation

### Install using pip

You’ll need to make sure you have pip available. You can check this by running:
```sh
pip --version
```

If you installed Python from source, with an installer from python.org, you should already have pip. If you’re on Linux and installed using your OS package manager, you may have to install pip separately.

> Haven’t installed pip? Visit: [https://pip.pypa.io/en/stable/installing/ ](https://pip.pypa.io/en/stable/installing/ )

Install the latest official release via pip. This is the best approach for most users. It will provide a stable version and are available for most platforms.

* Update pip to the latest stable version

```sh
pip3 install --upgrade pip
```

* Install Nirjas

```sh
pip3 install nirjas
```
- Upgrading Nirjas

Upgrade already installed Nirjas library to the latest version from [PyPI](https://pypi.org/).

```sh
pip3 install --upgrade Nirjas
```

### Install using source

If you are interested in contributing to [Nirjas](https://github.com/fossology/Nirjas) development, running the latest source code, or just like to build everything yourself, it is not difficult to install & build [Nirjas](https://github.com/fossology/Nirjas) from the source.

* Fork the [repo](https://github.com/fossology/Nirjas)

* Clone on your local system

```sh
git clone https://github.com/fossology/Nirjas.git
```

* Change directory

```sh
cd Nirjas/
```

* Install the package

```sh
pip3 install .
```

> This will install Nirjas on your system.


* Check if Nirjas is installed correctly or get help, Run:

    `nirjas -h` or `nirjas --help`

## Example Usage

- For help

```sh
nirjas -h
```

- To extract comments from a single file

```sh
nirjas -p <path to file>
```

- To extract comments from all the files in directory/sub-directory

```sh
nirjas -p <path to directory>
```

- To extract only source code (excludes commented part) out of a file

```sh
nirjas -i <target file> <new file name including extension>
```

or for default file generation (default file: source.txt)

```sh
nirjas -i <target file>
```

## Tests

To run a test for Nirjas, execute the following script:

```sh
python3 testScript.py
```
This will download all the test files into `nirjas/languages/tests/TestFiles` folder and will run the tests as well.

## Documentation

We maintain our entire documentation at GitHub wiki.
Feel free to switch from `code` to `wiki` or just click here - [Nirjas Documentation](https://github.com/fossology/Nirjas/wiki)


## Contributing

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

A detailed overview on how to contribute can be found in the [contributing guide](/CONTRIBUTING.md).

Feel free to ask questions or discuss suggestions on [Slack](https://fossology.slack.com/)

## License
This repository is licensed under the terms of [LGPL-2.1](/LICENSE). Check the [LICENSE](/LICENSE) file for more details.
