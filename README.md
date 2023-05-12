# Perceptest

[![Pytests with bazel](https://github.com/michael-hoss/perceptest/actions/workflows/pytest_with_bazel.yml/badge.svg)](https://github.com/michael-hoss/perceptest/actions/workflows/pytest_with_bazel.yml)

Test the object-based environment perception of automated driving systems.

This repo does it all, e.g.
- Convert various input data into a common format
- Use third-party software to compute metrics
- Compute perception algorithm benchmarking metrics (HOTA, MOTA etc.)
- Compare criticality metrics between reference and tested object lists to infer perception safety
- Analyze how well certain metrics are suitable for making certain statements about the perception quality
- *Change to try token access again*
