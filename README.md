<h1 align="center">Nirjas ~ নির্যাস</h1>

<p align="center"><i>A Python library for Comments and Source Code Extraction</i></p>

<p align="center">✨ 🍰 ✨</p>

<p align="center">

![python version](https://img.shields.io/badge/Python-v3.10%2B-blue)
![Unit Tests](https://github.com/fossology/Nirjas/workflows/Unit%20Tests/badge.svg)
![status](https://img.shields.io/pypi/status/Nirjas)
![License LGPL-2.1](https://img.shields.io/github/license/fossology/nirjas)
![release](https://img.shields.io/github/v/release/fossology/Nirjas)
[![Slack Channel](https://img.shields.io/badge/slack-fossology-blue.svg?longCache=true&logo=slack)](https://join.slack.com/t/fossology/shared_invite/enQtNzI0OTEzMTk0MjYzLTYyZWQxNDc0N2JiZGU2YmI3YmI1NjE4NDVjOGYxMTVjNGY3Y2MzZmM1OGZmMWI5NTRjMzJlNjExZGU2N2I5NGY)
![stars](https://img.shields.io/github/stars/fossology/nirjas?style=social)

</p>

## Description

A source code file usually contains various vital information such as license text, function/class documentation, code/logic explanation, etc in the form of comments (block & line).

Nirjas is a fully dedicated python library to extract the comments and source code out of your file(s). The extracted comments can be processed in various ways to detect licenses, generate documentation, process info, etc.

Apart from that the library serves you with all the required metadata about your Code, Comments and File(s)

For more details, read our [paper](https://arxiv.org/abs/2409.14609)

## Requirements

- Python 3.10+
- Poetry 2.0+ (for development/build workflows)

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
- Julia
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
- Sql
- TypeScript
- TSX

## Installation

### Install using pip

You’ll need to make sure you have pip available. You can check this by running:

```sh
pip --version
```

If you installed Python from source, with an installer from python.org, you should already have pip. If you’re on Linux and installed using your OS package manager, you may have to install pip separately.

> Haven’t installed pip? Visit: [https://pip.pypa.io/en/stable/installing/ ](https://pip.pypa.io/en/stable/installing/)

Install the latest official release via pip. This is the best approach for most users. It will provide a stable version and are available for most platforms.

- Update pip to the latest stable version

```sh
pip3 install --upgrade pip
```

- Install Nirjas

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

- Fork the [repo](https://github.com/fossology/Nirjas)

- Clone on your local system

```sh
git clone https://github.com/fossology/Nirjas.git
```

- Change directory

```sh
cd Nirjas/
```

- Install dependencies and package with Poetry

```sh
poetry install
```

- Optional: install into current environment with pip

```sh
pip3 install .
```

- Check if Nirjas is installed correctly or get help, Run:

  `nirjas -h` or `nirjas --help`

### Docker image

Nirjas also hosts Docker images on Docker hub. They can be pulled using

```sh
docker pull fossology/nirjas:latest
```

To scan with Docker image, just mount the directory you want to analyze and
pass the path as argument.

```sh
docker run --rm -v $(pwd):/opt/ fossology/nirjas:latest /opt/<file_to_analyze>
```

## Example Usage

- For help

```sh
nirjas -h
```

- To extract comments from a single file

```sh
nirjas <path to file>
```

- To extract strings which assigned to variables from a source code file (Not yet implemented)

```sh
nirjas <path to source code file>
```

- To extract comments from all the files in directory/sub-directory

```sh
nirjas <path to directory>
```

- To extract only source code (excludes commented part) out of a file

```sh
nirjas -i <target file> <new file name including extension>
```

or for default file generation (default file: source.txt)

```sh
nirjas -i <target file>
```

## License Gate (ML)

Nirjas ships an optional **recall-first license gate** — a lightweight binary
classifier that answers *"is this text actual license text worth routing to
[Atarashi](https://github.com/fossology/atarashi)?"*. It is meant as a cheap
pre-filter: cull the obvious non-license comments Nirjas already extracts so the
expensive license scanner only runs on candidates that matter.

### Approach

- **Model:** a [model2vec](https://github.com/MinishLab/model2vec) static
  embedding (`minishlab/potion-base-32M`) with a scikit-learn logistic head.
  Inference is **torch-free** — static embeddings mean no deep-learning runtime,
  so the gate loads in milliseconds and runs on CPU.
- **Recall-first, not argmax.** The decision uses a tuned threshold of **0.20**,
  not the default 0.5. Missing a license is the costly error; a false positive
  just wastes one Atarashi call. So the operating point is chosen to catch
  (almost) every license at the price of a small false-positive rate.
- **Quality gate on release.** Training is deterministic (`random_seed=0`) and a
  build only publishes if it clears `license_recall ≥ 0.99` and `FPR ≤ 0.05` on
  the held-out test split.

Validated metrics (`rycerzes/nirjas-dataset`, splits 55,610 / 6,877 / 6,895):

| Evaluation           | License recall | False-positive rate |
| -------------------- | -------------- | ------------------- |
| Held-out test split  | 0.9952         | 0.0227              |
| Real-corpus sample   | 1.0000         | 0.0133              |

Full methodology, dataset construction, and benchmarks are in the
[Nirjas benchmark report](https://github.com/fossology/gsoc/blob/main/docs/2026/enhancing-atarashi/updates/nirjas-benchmark-report.md).

### Usage

```sh
pip install 'nirjas[gate]'
```

```python
from nirjas.gate import load_gate, classify

pipe, threshold = load_gate()                 # downloads rycerzes/nirjas-gate from HF Hub (cached)
classify(pipe, ["// SPDX-License-Identifier: MIT"], threshold)  # -> [True]
```

### Retraining

The model is published to the Hugging Face Hub; retraining is only needed to
reproduce or update it. Install the training stack and run the script (CI
publishes via `workflow_dispatch`):

```sh
poetry install --with train
poetry run python scripts/train_and_release.py --output-dir trained_gate
```

## Tests

To run tests for Nirjas, download the Tree-Sitter parsers and run pytest:

```sh
python3 scripts/download_parsers.py
pytest
```

The suite is offline: every test input lives in `tests/data`, so nothing is
downloaded at test time.

It has two tiers:

- **`tests/data/fixtures`** — small hand-written files we own, one per language
  aimed at that language's hardest case (a `-->` operator versus a `--` comment
  in Haskell, `'` as transpose versus a quote in MATLAB, `${x##*/}` expansion in
  shell, a regex literal holding `//` in JavaScript), plus cross-cutting edge
  cases: CRLF, a BOM, no trailing newline, an unterminated block, nesting.
- **`tests/data/corpus`** — three real-world files per language, vendored
  verbatim from permissively licensed upstreams at pinned commits. Real code
  carries licence headers, doc-comment conventions and hundreds of comments that
  no hand-written fixture thinks to include. Every vendored file has an `.ABOUT`
  sidecar recording origin, pinned commit and licence. Run just these with
  `pytest -m corpus`.

Both tiers assert the same way: a `.expected.json` for extractor output and a
`.expected.src` for the stripped source, with the invariant checks running
alongside. Nobody reads a 600-line golden top to bottom, and nobody needs to —
you read the *diff* when behaviour changes.

When a change *should* alter output, review the diff and re-record the goldens:

```sh
NIRJAS_REGEN_FIXTURES=1 pytest
```

Regeneration rewrites goldens from current behaviour, so always read the
resulting diff before committing it. The invariant checks still run in this
mode, which is what stops a golden from enshrining a broken result.

## Linting and Type Checking

```sh
poetry run ruff check .
poetry run pyright
```

## Documentation

We maintain our entire documentation at GitHub wiki.
Feel free to switch from `code` to `wiki` or just click here - [Nirjas Documentation](https://github.com/fossology/Nirjas/wiki)

## Contributing

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

A detailed overview on how to contribute can be found in the [contributing guide](/CONTRIBUTING.md).

Feel free to ask questions or discuss suggestions on [Slack](https://fossology.slack.com/)

## License

This repository is licensed under the terms of [LGPL-2.1](/LICENSE). Check the [LICENSE](/LICENSE) file for more details.

## Citation

If you find this project useful, please consider giving a star ⭐ and please cite as:

```
@INPROCEEDINGS{9734222,
  author={Bhardwaj, Ayush and Sahil and Pratap, Kaushlendra and Mishra, Gaurav},
  booktitle={2022 12th International Conference on Cloud Computing, Data Science & Engineering (Confluence)}, 
  title={Nirjas: An open source framework for extracting metadata from the source code}, 
  year={2022},
  pages={47-52},
  doi={10.1109/Confluence52989.2022.9734222}}

```


