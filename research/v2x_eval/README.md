# Evaluate custom tracking data using nuScenes tracking metrics

#### Preparations

- TODO: make this just a tutorial for nuscenes custom data evaluation, no longer about artery or v2x
- TODO: upload mini dataset to sciebo for CI and blog post readers!

- Do the set ups from this repo's main `README.md` and potentially also from `CONTRIBUTING.md`.
- Have the unzipped artery simulation logs available on disk with subdirs `simXXdata/results_YY`
- Activate your Python environment with all dependencies installed
- Call help to see how to use the CLI options (and look at default values in the code)

```bash
bazel run //research/v2x_eval:main -- --help
```

#### Run the code 

```bash
bazel run //research/v2x_eval:main  # specify own values to CLI options if needed
```

#### Debug the code

```bash
# First, manually set your breakpoints in VSCode. Then:
export DEBUG=1
bazel run //research/v2x_eval:main
# The code will wait at the beginning.
# Now, launch the "Python: Attach" debug config in VSCode
```
