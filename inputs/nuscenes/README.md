# nuScenes Dataset as input data

### Setup of the nuScenes devkit
This repo uses a local fork of `nuscenes-devkit` instead of the pip version. 

This repo's setup instructions also make sure that the nuscenes things work well.

Note: installing the local fork as an editable pip package crashes. Instead, we just 
have the code here and append its root to the PYTHONPATH (somewhat ugly, but that's what they support).

### Usage tutorial
For a tutorial, see
```bash
jupyter notebook third_party/nuscenes_devkit/python_sdk/tutorials/nuscenes_tutorial.ipynb
```

### Role of the dataset

The official nuscenes dataset is *not* needed to make use of the devkit's functionality for converted own data.

However, some manual local-only tests use the official dataset and require it to be downloaded to the specified dir `/data/sets/nuscenes`.


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
