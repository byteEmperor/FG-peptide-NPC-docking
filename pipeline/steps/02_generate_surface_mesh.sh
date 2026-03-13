#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# 01_preprocess_proteins.sh (version-controlled)
# -----------------------------------------------------------------------------

set -e
set -x

# ---------------------- ARGUMENTS & DEFAULTS ----------------------
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PIPELINE_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_DIR="$(dirname "$PIPELINE_DIR")"

DATA_DIR=${PROJECT_DIR}/data

INPUT_DIR=${1:-${DATA_DIR}/processed/proteins}
OUTPUT_DIR=${2:-${DATA_DIR}/processed/meshes}
N_JOBS=${3:-8}
CONTAINER_NAME=${4:-docker_pipeline-surface_mesh}
PROTEIN=${5:-$DATA_DIR/processed/proteins/ntf2_processed.pdb}
LIGAND=${6:-$DATA_DIR/raw/ligands/01_GPG.sdf}

# ---------------------- DERIVE IDS & PATHS ----------------------
# ---------------------- DERIVE IDS & PATHS ----------------------
PROTEIN_BASENAME=$(basename "$PROTEIN" .pdb)
LIGAND_BASENAME=$(basename "$LIGAND" | sed 's/\.[^.]*$//')  # remove extension
RUN_TIMESTAMP=$(date +%Y%m%d_%H%M%S)                        # unique timestamp
RUN_FOLDER="$OUTPUT_DIR/${PROTEIN_BASENAME}_${LIGAND_BASENAME}_$RUN_TIMESTAMP"

mkdir -p "$RUN_FOLDER"

MESH_OUTPUT="$RUN_FOLDER/${PROTEIN_BASENAME}_${LIGAND_BASENAME}_${RUN_TIMESTAMP}_surface.ply"

# ---------------------- RUN DOCKER MESH GENERATION ----------------------
docker run --rm \
    -v "$(dirname "$PROTEIN")":/input_protein \
    -v "$(dirname "$LIGAND")":/input_ligand \
    -v "$RUN_FOLDER":/output \
    -v "$PROJECT_DIR/surfdock":/workspace/surfdock \
    -e PYTHONPATH=/workspace \
    "$CONTAINER_NAME" \
    conda run -n surface_mesh python /workspace/surfdock/surface_mesh/compute_target_mesh.py \
        --protein "/input_protein/$(basename "$PROTEIN")" \
        --ligand "/input_ligand/$(basename "$LIGAND")" \
        --output "/output/surface.ply" \
        --full_protein

# ---------------------- RENAME OUTPUT ----------------------
mv "$RUN_FOLDER/surface.ply" "$MESH_OUTPUT"

# ---------------------- CREATE METADATA.JSON ----------------------
cat > "$RUN_FOLDER/metadata.json" <<EOF
{
  "protein": "$PROTEIN_BASENAME",
  "ligand": "$LIGAND_BASENAME",
  "mesh_file": "$(basename "$MESH_OUTPUT")",
  "n_jobs": $N_JOBS,
  "container": "$CONTAINER_NAME"
}
EOF

echo "[INFO] Mesh generated and saved to $MESH_OUTPUT"
echo "[INFO] Metadata saved to $RUN_FOLDER/metadata.json"
