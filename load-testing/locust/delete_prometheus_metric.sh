#!/bin/bash

PROMETHEUS_URL="http://localhost:9090"
METRIC_NAME=$1
TIME_RANGE=$2

if [ -z "${METRIC_NAME}" ]; then
  echo "Please provide the metric name as the first argument"
  exit 1
fi

if [ -z "${TIME_RANGE}" ]; then
  echo "Please provide the time range as the second argument"
  exit 1
fi

curl -X POST \
  -g "${PROMETHEUS_URL}/api/v1/admin/tsdb/delete_series" \
  --data-urlencode "match[]={__name__='${METRIC_NAME}'}" \
  --data-urlencode "start=$(date -u -d "${TIME_RANGE} ago" +%s)" \
  --data-urlencode "end=$(date -u +%s)"
