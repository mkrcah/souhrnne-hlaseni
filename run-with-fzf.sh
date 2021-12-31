#!/usr/bin/env bash

set -u # fail on unset variable
set -o pipefail # fail on pipe error
set -e  # fail on error

# where generated reports will be stored
REPORTS_DIR=generated_reports

YEAR=$(seq 2021 2030 | fzf)
MONTH=$(seq -w 1 12 | fzf)

mkdir -p $REPORTS_DIR
OUTPUT_FILENAME=$REPORTS_DIR/dphsh-"$YEAR-$MONTH".xml

python3 main.py \
  --year="$YEAR" \
  --month="$MONTH"  \
  --path-to-static-details=./my-static-data.yml > "$OUTPUT_FILENAME"

echo "Report stored in $OUTPUT_FILENAME"