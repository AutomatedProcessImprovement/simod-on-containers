# Deployment on kind

Before everything, make sure there is a folder at `/tmp/simod-volume` on the host machine. This folder will be mounted as a volume in the cluster and used for storing user inputs and BPS discovery results.

Create a cluster with 2 workers, for example:

```shell
./run.sh kind-cluster-1-workers.yaml 
```

The helper script will:

- create a cluster,
- deploy the monitoring solution,
- deploy simod-on-containers dependencies,
- deploy simod-on-containers.

To delete the cluster, use:

```shell
kind delete cluster 
```

To check if simod-on-container pods are running, use:

```shell
kubectl get pods
```

To make expose Web API to the host, use:

```shell
kubectl port-forward service/simod-http 8000:8000
```

To expose Grafana to the host, use:

```shell
kubectl port-forward -n monitoring service/grafana 3000:3000
```

Simod's Grapha dashboard is located in the `./monitoring/grafana/` folder. Use the JSON file inside to import the dashboard through the Grafana UI.

To run load testing with Locust, use:

```shell
kubectl apply -f deploy/kind/locust-scalability-travel.yaml
```
