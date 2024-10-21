# Evaluate custom tracking data using nuScenes tracking metrics

#### Preparations

- Do the set ups from this repo's main `README.md` and potentially also from `CONTRIBUTING.md`.
- Activate your Python environment with all dependencies installed and ENV variables set.

#### Run the code 

```bash
bazel run //research/v2x_eval:main
```

#### Debug the code

```bash
# First, manually set your breakpoints in VSCode. Then:
export DEBUG=1
bazel run //research/v2x_eval:main
# The code will wait at the beginning.
# Now, launch the "Python: Attach" debug config in VSCode
```
