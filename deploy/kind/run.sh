#!/usr/bin/env bash

CLUSTER_CONFIG=$1
if [ -z "$CLUSTER_CONFIG" ]; then
    echo "Cluster config is required"
    exit 1
fi

# creating kind cluster
kind create cluster --config $CLUSTER_CONFIG

# setting up monitoring and simod-on-containers dependencies
kubectl apply --server-side -f simod-full/monitoring/setup
kubectl apply --server-side -f simod-full/monitoring/
kubectl apply -f simod-full/setup

# getting node names in the cluster
NODE_NAMES=`/opt/homebrew/bin/kind get nodes`
# converting node names to a string
NODE_NAMES_STRING=`echo $NODE_NAMES | tr ' ' ','`
# filtering out kind-control-plane
NODE_NAMES_STRING=`echo $NODE_NAMES_STRING | sed 's/kind-control-plane,//'`
NODE_NAMES_STRING=`echo $NODE_NAMES_STRING | sed 's/,kind-control-plane//'`

# loading docker images to the worker nodes
kind load docker-image --nodes $NODE_NAMES_STRING nokal/simod-http:0.11.1
kind load docker-image --nodes $NODE_NAMES_STRING nokal/simod-job-controller-go:0.6.0
kind load docker-image --nodes $NODE_NAMES_STRING nokal/simod-load-testing:0.2.1
kind load docker-image --nodes $NODE_NAMES_STRING nokal/simod:3.3.0

# setting up simod-on-containers
kubectl apply -f simod-full/apps
