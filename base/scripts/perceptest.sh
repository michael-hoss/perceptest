# This script makes sure that the perceptest repo runs well.
# Put it into your .bashrc file to make it work.

# Include it like this in your .bashrc file:
# conda activate research  # need to be in the used Python evironment before sourcing this
# export PERCEPTEST_REPO=<path to perceptest repo>`
# source $PERCEPTEST_REPO/base/scripts/perceptest.sh

echo "Setting up perceptest environment"
source $PERCEPTEST_REPO/inputs/nuscenes/nuscenesrc.sh
