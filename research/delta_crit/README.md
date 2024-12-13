# DeltaCrit

Assess whether the perception under test underestimates or overestimates the criticality of the current scene or scenario.

## Installation

Besides the `requirements.txt` file, you also need

```bash
pip install -e $PERCEPTEST_REPO/third_party/commonroad-crime
```

to use the latest referenced version from the submodule. 
This is on purpose not included in `requirements.txt` because it confuses dependabot.

## Testing

For now, I will do without bazel. Just run

`pytest`
