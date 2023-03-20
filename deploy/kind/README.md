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

https://github.com/deliveryhero/helm-charts/tree/master/stable/locust
https://docs.locust.io/en/stable/running-in-docker.html

```shell
helm repo add deliveryhero https://charts.deliveryhero.io/
#kubectl create configmap locustfile --from-file ../../load-testing/locust/main.py
helm install locust deliveryhero/locust \
--set loadtest.name=simod \
--set loadtest.locust_host=http://simod-http \
--set master.image=nokal/locust:2.15.1 \
--set worker.image=nokal/locust:2.15.1
kubectl --namespace default port-forward service/locust 8089:8089
```

## Mongo

```shell
kubectl apply -f mongo.yaml
```