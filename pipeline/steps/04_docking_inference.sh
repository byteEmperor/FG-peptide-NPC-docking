#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# 04_docking_inference.sh
# -----------------------------------------------------------------------------

set -e
set -x

# ---------------------- PATH SETUP ----------------------

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PIPELINE_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_DIR="$(dirname "$PIPELINE_DIR")"

DATA_DIR=${PROJECT_DIR}/data
MODEL_DIR=/workspace/surfdock/model_weights

CSV_FILE=${1:-$DATA_DIR/processed/docking_input.csv}
ESM_EMBEDDING=${2:-$DATA_DIR/processed/esm_embeddings/ntf2_processed/esm_output/ntf2_processed.pdb_chain_0.pt}
OUTPUT_DIR=${3:-$DATA_DIR/results/surfdock/docking}

CONTAINER_NAME=${4:-docker_pipeline-docking_inference}

mkdir -p "$OUTPUT_DIR"

# ---------------------- MODEL PATHS ----------------------

DIFFUSION_MODEL=${MODEL_DIR}/docking
CONFIDENCE_MODEL=${MODEL_DIR}/posepredict

# ---------------------- RUN DOCKING ----------------------

docker run --rm \
    -v "$PROJECT_DIR/surfdock":/workspace/surfdock \
    -v "$DATA_DIR":/data \
    -e PYTHONPATH=/workspace \
    "$CONTAINER_NAME" \
    conda run -n docking_inference python /workspace/surfdock/docking_inference/inference_accelerate.py \
        --data_csv /data/processed/docking_input.csv \
        --model_dir /workspace/surfdock/model_weights/docking \
        --ckpt best_ema_inference_epoch_model.pt \
        --confidence_model_dir /workspace/surfdock/model_weights/posepredict \
        --confidence_ckpt best_model.pt \
        --esm_embeddings_path /data/processed/esm_embeddings/ntf2_processed/esm_output/ntf2_processed.pdb_chain_0.pt \
        --out_dir /data/results/surfdock/docking \
        --samples_per_complex 4 \
        --save_docking_result \
        --inference_mode evaluate \
        --batch_size 4 \
        --batch_size_molecule 1