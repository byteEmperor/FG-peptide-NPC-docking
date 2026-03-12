#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# generate_surface.sh (version-controlled)
# -----------------------------------------------------------------------------

set -e

# ---------------------- ARGUMENTS & DEFAULTS ----------------------
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PIPELINE_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_DIR="$(dirname "$PIPELINE_DIR")"

DATA_DIR=${PROJECT_DIR}/data

INPUT_DIR=${1:-${DATA_DIR}/raw/samples}
OUTPUT_DIR=${2:-${DATA_DIR}/processed/surfaces}
N_JOBS=${3:-8}
CONTAINER_NAME=${4:-docker_pipeline-surface_mesh}
WORKFLOWS_DIR=${5:-${PIPELINE_DIR}/workflows}   # directory where metadata_manager.py lives

METADATA_CSV="$OUTPUT_DIR/surface_metadata.csv"

mkdir -p "$OUTPUT_DIR"

# ---------------------- GENERATE METADATA CSV ----------------------
echo "[INFO] Checking sample versions and generating metadata CSV..."
python "$WORKFLOWS_DIR/metadata_manager.py" \
    --input_dir "$INPUT_DIR" \
    --output_dir "$OUTPUT_DIR" \
    --csv_file "$METADATA_CSV"

# ---------------------- PROCESS EACH SAMPLE ----------------------
echo "[INFO] Starting surface processing..."

while IFS=, read -r sample_name processed_path needs_reprocessing || [ -n "$sample_name" ]; do

    needs_reprocessing=$(echo "$needs_reprocessing" | tr -d '\r')

    # Skip header
    if [ "$sample_name" == "sample_name" ]; then
        continue
    fi

    if [ "$needs_reprocessing" != "True" ]; then
        echo "[SKIP] $sample_name (up-to-date)"
        continue
    fi

    sample_input="$INPUT_DIR/$sample_name"
    sample_output="$OUTPUT_DIR/$sample_name"
    mkdir -p "$sample_output"

    echo "[START] Processing sample: $sample_name"

    echo "  > Reducing protein with OpenBabel..."
    docker run --rm \
        -v "$INPUT_DIR":/input \
        -v "$OUTPUT_DIR":/output \
        -v "$PROJECT_DIR/surfdock":/surfdock \
        "$CONTAINER_NAME" \
        conda run -n surface_mesh python /surfdock/surface_mesh/openbabel_reduce.py \
            --protein /input/"$sample_name"/"1A0Q.pdb" \
            --outdir /output/"$sample_name"

    echo "  > Generating surface mesh..."
    docker run --rm \
        -v "$INPUT_DIR":/input \
        -v "$OUTPUT_DIR":/output \
        "$CONTAINER_NAME" \
        python /surfdock/comp_surface/prepare_target/computeTargetMesh_test_samples.py \
            --data_dir /input/"$sample_name" \
            --out_dir /output/"$sample_name" \
            --n_jobs "$N_JOBS"

    echo "[DONE] Sample processed: $sample_name"

done < "$METADATA_CSV"

echo "[INFO] All surface samples processed."