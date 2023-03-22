# Deployment on kind

## RabbitMQ

```shell
kubectl apply -f rabbitmq.yaml
```

## Prometheus & Grafana

https://prometheus-operator.dev/docs/prologue/quick-start/

```shell
git clone https://github.com/prometheus-operator/kube-prometheus.git
cd kube-prometheus
kubectl create -f manifests/setup
kubectl create -f manifests/
kubectl --namespace monitoring port-forward svc/prometheus-k8s 9090
kubectl --namespace monitoring port-forward svc/alertmanager-main 9093
kubectl --namespace monitoring port-forward svc/grafana 3000
kubectl delete --ignore-not-found=true -f manifests/ -f manifests/setup
```

## Kubernetes Metrics

https://github.com/kubernetes-sigs/metrics-server
https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/
https://kubernetes.io/docs/concepts/cluster-administration/system-metrics/

```shell
kubectl apply -f metrics-server.yaml
```

## Locust

```shell
kubectl apply -f locust.yaml
```

## Mongo

```shell
kubectl apply -f mongo.yaml
```