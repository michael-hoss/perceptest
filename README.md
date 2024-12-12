# Perceptest

[![Pytests with bazel](https://github.com/michael-hoss/perceptest/actions/workflows/pytest_with_bazel.yaml/badge.svg)](https://github.com/michael-hoss/perceptest/actions/workflows/pytest_with_bazel.yaml)

Test the object-based environment perception of automated driving systems.

## Directory structure

- `base`: multi-purpose utilities and functional code
- `inputs`: read input data and convert them to needed formats
    - `artery`: read logs from the Artery simulator; convert to nuScenes format
    - `nuscenes`: helpers for the nuScenes 3D object tracking evaluation
- `research`: code for specific academic publications
    - `v2x_eval`: Evaluate own object tracking data on nuscenes tracking metrics
    - `delta_crit`: (WIP) Compare criticality metrics between reference and tested object lists to infer perception safety
    - `metric_bench`: (TBD) Analyze how well certain metrics can make statements about the perception quality
- `third_party`: third-party software as git submodules

## Run the code on your own

- Create a Python 3.10 environment for perceptest via miniconda or similar
- Install the Python requirements into your environment: `pip install -r requirements.txt`
- Install [bazel](https://bazel.build/)
    - Via [bazelisk](https://github.com/bazelbuild/bazelisk), you automatically get the version given in `.bazelversion`
    - The most basic way is to download bazelisk's released binaries, place them under `/usr/local/bin/`, and make them executable
- Run an executable with `bazel run //path/to:executable`


## Contribute to perceptest

See [CONTRIBUTING.md](CONTRIBUTING.md).
