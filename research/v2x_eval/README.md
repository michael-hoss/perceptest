# Evaluating collaborative V2X perception using object tracking metrics

## Execute code on your own

- Do the set ups from this repo's main `README.md`
- Have the unzipped artery simulation logs available on disk with subdirs `simXXdata/results_YY`
- Know where you want to generate the converted nuscenes files, e.g., `/data/sets/nuscenes`
    - Download the nuScenes dataset to `data/sets/nuscenes` -> Is this needed at all???
- Call the following executable with the correct input arguments (see `main.py`)

```bash
export DEBUG=1
bazel run //research/v2x_eval:main
```
