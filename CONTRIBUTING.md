# Contributing

## Installations

- See the [README.md](README.md) for general installation instructions
- `pip install -r requirements-dev.txt` for the common developer dependencies
- `cd research/subdir_name && pip install -r requirements.txt` for the dependencies of the respective project.
- Install [buildifier](https://github.com/bazelbuild/buildtools/blob/master/buildifier/README.md) to format bazel files. The most basic way is to download the released binary, place it under `/usr/local/bin/`, and make it executable.

## Environment variables

- Copy the `perceptestrc.sh` script to your python environment activation hook (for `bazel run`)
- Copy the `.env_bazel_test_default` to the git-ignored `.env` (for `bazel test`)
- If necessary, adapt the paths in these files to locally valid paths on your machine

## Pre-commit hooks

- Install the pre-commit hooks: `pre-commit install`
  - This will use `.pre-commit-config.yaml`
- To run these hooks manually, use `pre-commit run --all-files`

## Get active

- Run tests: `bazel test //...`
- Debug an individual test: `bazel test //path/to:test_target --test_env=DEBUG=1 --test_timeout=3600`
  - Attach to the debugger after some seconds with "Python: Attach" in VSCode
  
