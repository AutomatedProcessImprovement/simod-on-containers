#!/usr/bin/env ruby

# kind create cluster --config kind-cluster.yaml
puts `kind load docker-image nokal/simod-queue-worker:0.0.0`
puts `kind load docker-image nokal/simod-http:0.2.0`
puts `kubectl create -f https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.3/examples/celery-rabbitmq/rabbitmq-service.yaml`
puts `kubectl create -f https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.3/examples/celery-rabbitmq/rabbitmq-controller.yaml`
puts `kubectl apply -f deployment.yaml`
puts `kubectl port-forward deploy/simod-http :8000`