# Contributing

## Installations

- See the [README.md](README.md) for general installation instructions
- `pip install -r requirements-dev.txt` for developer dependencies
- Install [buildifier](https://github.com/bazelbuild/buildtools/blob/master/buildifier/README.md) to format bazel files. The most basic way is to download the released binary, place it under `/usr/local/bin/`, and make it executable.

## Environment variables

- Copy the `perceptestrc.sh` script to your python environment activation hook (see instructions there)
- Copy the `.env_bazel_test_default` to the git-ignored `.env` to specify how bazel tests will operate locally.

## Pre-commit hooks

- Install the pre-commit hooks: `pre-commit install`
  - This will use `.pre-commit-config.yaml`
- To run these hooks manually, use `pre-commit run --all-files`
