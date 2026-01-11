#!/usr/bin/env bash
set -euo pipefail

# Example:
#   ./scripts/run_local.sh data/lap_times.csv

INPUT="${1:-}"
if [[ -z "${INPUT}" ]]; then
  echo "Usage: $0 <input_csv_path> [extra args...]"
  exit 1
fi

shift || true

python -m your_project.jobs.main_job \
  --master "local[*]" \
  --input "${INPUT}" \
  "$@"