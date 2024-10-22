# This script initializes ENV variables so that `bazel run` commands work well.
# Note: for `bazel test`, use `.env`!

# If you want different paths on your local system, create an own perceptestrc.sh 
# file and set these variables as you wish.

# You may want to put it into the activation hook of your related python environment.
# For miniconda, this is ~/miniconda3/envs/perceptest/etc/conda/activate.d/perceptestrc.sh


echo "Setting up perceptest environment"

# Path to the perceptest repo
export PERCEPTEST_REPO="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

# Paths to local datasets.
# If these paths are not set or data is missing there, some functionality might not work.
export NUSCENES="/data/sets/nuscenes"  # need to download it there manually
export ARTERY_DATA_ROOT="/tmp/artery_data/run"  # code will download data there

# Set PYTHONPATH for dependencies that need that
nuscenes_devkit_path="$PERCEPTEST_REPO/third_party/nuscenes-devkit/python-sdk"
if [ -z "$PYTHONPATH" ]; then
  export PYTHONPATH="$nuscenes_devkit_path"
else
  export PYTHONPATH="$PYTHONPATH:$nuscenes_devkit_path"
fi
