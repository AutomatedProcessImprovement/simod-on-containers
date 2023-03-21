#!/usr/bin/env bash


timestamp=$(date +%Y%m%d%H%M%S)
output_dir="$REPORT_OUTPUT_DIR/$timestamp"
mkdir -p "$output_dir"

k6 run \
--vus $K6_VUS \
--duration $K6_DURATION \
--rps $K6_RPS \
--out csv=$output_dir/stats.csv \
--no-usage-report \
--discard-response-bodies \
$SCRIPT_NAME