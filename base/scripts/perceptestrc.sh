# This script initializes things so that the perceptest repo runs well.
# Put it into the activation hook of your perceptest python environment.
# For miniconda, this is ~/miniconda3/envs/env_name/etc/conda/activate.d/perceptest.sh

echo "Setting up perceptest environment"
export PERCEPTEST_REPO=<path to your perceptest repo>
source $PERCEPTEST_REPO/inputs/nuscenes/nuscenesrc.sh

source $PERCEPTEST_REPO/inputs/artery/arteryrc.sh
