#!/usr/bin/env bash

# This script is used to construct a simple run with SurfDock, docking a small ligand with no pose scoring

project_root=$(realpath "$(dirname "$(readlink -f "$0")")/..")

#------------------------------------------------------------------------------------------------#
#------------------------------------ Step0 : Setup Params --------------------------------------#

data_raw=${project_root}/data/raw/samples
data_processed=${project_root}/data/processed



