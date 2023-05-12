# nuScenes Dataset as input data

### Setup of the nuScenes devkit
This repo uses a local fork of `nuscenes-devkit` instead of the pip version
- Install its requirements through the top-level `requirements.txt`
- Add the code of the `nuscenes-devkit` fork under `third_party` to the `PYTHONPATH`, as explained in [the official tutorial](https://github.com/nutonomy/nuscenes-devkit/blob/master/docs/installation.md#setup-pythonpath)
- Set the environment variable `NUSCENES`
- :information_source: When I execute nuscenes-devkit code through bazel, bazel takes care of Python path and environment variables.

Note: installing the local fork as an editable pip package crashes and is also not mentioned in the official tutorial. However, the solution with setting the Python path works fine.

### Usage tutorial
For a tutorial, see
```bash
jupyter notebook third_party/nuscenes_devkit/python_sdk/tutorials/nuscenes_tutorial.ipynb
```

### Evaluate nuScenes example data

I call the nuscenes evaluation code directly through Python instead of using the CLI. However, this is how it would look like in the CLI.

On the predefined `val` split:
```bash
python third_party/nuscenes-devkit/python-sdk/nuscenes/eval/tracking/evaluate.py \
/data/sets/tracking-megvii/results_val_megvii.json \
--output_dir ~/git/perceptest/inputs/nuscenes/tracking_eval_outputs_megvii_val \
--eval_set val \
--dataroot /data/sets/nuscenes \
--version v1.0-trainval \
--verbose 1
```

On a custom `mini_custom_val` split:
```bash
python third_party/nuscenes-devkit/python-sdk/nuscenes/eval/tracking/evaluate.py \
/data/sets/tracking-megvii/results_val_megvii.json \
--output_dir /data/sets/tracking-megvii/eval_outputs_on_custom_mini_split \
--eval_set mini_custom_val \
--dataroot /data/sets/nuscenes \
--version v1.0-trainval \
--verbose 1
```
