#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# 02_compute_esm_embeddings.sh
# -----------------------------------------------------------------------------

set -e
set -x

# ---------------------- PATH SETUP ----------------------

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PIPELINE_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_DIR="$(dirname "$PIPELINE_DIR")"

DATA_DIR=${PROJECT_DIR}/data

PROTEIN=${1:-$DATA_DIR/processed/proteins/ntf2_processed.pdb}
OUTPUT_DIR=${2:-$DATA_DIR/processed/esm_embeddings}
CONTAINER_NAME=${3:-docker_pipeline-esm_embedding}
CONTAINER_NAME2=docker_pipeline-esm

PROTEIN_BASENAME=$(basename "$PROTEIN" .pdb)

RUN_FOLDER="$OUTPUT_DIR/$PROTEIN_BASENAME"

mkdir -p "$RUN_FOLDER"

FASTA_FILE="$RUN_FOLDER/${PROTEIN_BASENAME}.fasta"
EMBEDDING_DIR="$RUN_FOLDER/esm_output"

# ---------------------- EXTRACT FASTA ----------------------

docker run --rm \
    -v "$(dirname "$PROTEIN")":/input_protein \
    -v "$RUN_FOLDER":/output \
    -v "$PROJECT_DIR/surfdock":/workspace/surfdock \
    "$CONTAINER_NAME" \
    conda run -n esm_embedding python /workspace/surfdock/esm_embedding/datasets/esm_embedding_preparation.py \
        --protein_path "/input_protein/$(basename "$PROTEIN")" \
        --out_file "/output/${PROTEIN_BASENAME}.fasta"

# ---------------------- RUN ESM MODEL ----------------------

docker run --rm \
    -v "$RUN_FOLDER":/output \
    -v "$PROJECT_DIR/esm":/workspace/esm \
    -e PYTHONPATH=/workspace/esm/esm \
    "$CONTAINER_NAME2" \
    conda run -n esmfold python /workspace/esm/esm/scripts/extract.py \
        esm2_t33_650M_UR50D \
        "/output/${PROTEIN_BASENAME}.fasta" \
        "/output/esm_output" \
        --repr_layers 33 \
        --include per_tok \
        --truncation_seq_length 4096

echo "[INFO] ESM embeddings saved to $EMBEDDING_DIR"