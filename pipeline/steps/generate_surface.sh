#!/bin/bash
# -----------------------------------------------------------------------------
# generate_surface.sh (version-controlled)
# -----------------------------------------------------------------------------

set -e

# ---------------------- ARGUMENTS & DEFAULTS ----------------------
INPUT_DIR=${1:-data/raw/samples}
OUTPUT_DIR=${2:-data/processed/surfaces}
N_JOBS=${3:-8}
CONTAINER_NAME=${4:-surfdock_surface}
WORKFLOWS_DIR=${5:-workflows}   # directory where metadata_manager.py lives

METADATA_CSV="$OUTPUT_DIR/surface_metadata.csv"

mkdir -p "$OUTPUT_DIR"

# ---------------------- GENERATE METADATA CSV ----------------------
echo "[INFO] Checking sample versions and generating metadata CSV..."
python "$WORKFLOWS_DIR/metadata_manager.py" \
    --output_dir "$OUTPUT_DIR" \
    --csv_file "$METADATA_CSV"

# ---------------------- PROCESS EACH SAMPLE ----------------------
echo "[INFO] Starting surface processing..."
while IFS=, read -r sample_name processed_path needs_reprocessing; do
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

    # Step 1: Protein preprocessing
    echo "  > Reducing protein with OpenBabel..."
    docker run --rm \
        -v "$INPUT_DIR":/input \
        -v "$OUTPUT_DIR":/output \
        "$CONTAINER_NAME" \
        python /surfdock/comp_surface/protein_process/openbabel_reduce_openbabel.py \
            --data_path /input/"$sample_name" \
            --save_path /output/"$sample_name" \
            --n_jobs "$N_JOBS"

    # Step 2: Surface mesh generation
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