# Contributing

## Installations

- Create a Python 3.10 environment for perceptest via miniconda or similar
- Install the Python requirements into your environment: `pip install -r requirements-dev.txt`
- Install [bazelisk](https://github.com/bazelbuild/bazelisk) and [buildifier](https://github.com/bazelbuild/buildtools/blob/master/buildifier/README.md). The most basic way is to download released binaries, place them under `/usr/local/bin/`, and make them executable.

## Environment variables

- Source the `scripts/perceptest.sh` file in your `.bashrc` file (see prerequisites there)

## Pre-commit hooks

- Install the pre-commit hooks: `pre-commit install`
  - This will use `.pre-commit-config.yaml`
- To run these hooks manually, use `pre-commit run --all-files`
