echo "Setting up nuScenes environment"

# Define path to local nuscenes dataset.
export NUSCENES="/data/sets/nuscenes"
# export NUIMAGES="/data/sets/nuimages" # not used yet


# Add the nuscenes-devkit to the python path, as demanded by the nuscenes documentation.
nuscenes_devkit_path="$PERCEPTEST_REPO/third_party/nuscenes-devkit/python-sdk"
if [ -z "$PYTHONPATH" ]; then
  export PYTHONPATH="$nuscenes_devkit_path"
else
  export PYTHONPATH="$PYTHONPATH:$nuscenes_devkit_path"
fi
