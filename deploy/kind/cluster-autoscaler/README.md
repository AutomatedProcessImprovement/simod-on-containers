# Cluster API (CAPI)

https://cluster-api.sigs.k8s.io/user/quick-start.html

It's a reference implementation of a Kubernetes cluster manager. Using Docker as a provider, we can extend `kind` and use the cluster autoscaler.


## Getting Started

```shell
kind create cluster --config kind-cluster-with-extramounts.yaml 

export EXP_CLUSTER_RESOURCE_SET=true
export EXP_MACHINE_POOL=true
export CLUSTER_TOPOLOGY=true
export EXP_RUNTIME_SDK=true
export EXP_LAZY_RESTMAPPER=true

clusterctl init --infrastructure docker
clusterctl generate cluster capi-simod --flavor development \
  --kubernetes-version v1.26.0 \
  --control-plane-machine-count=1 \
  --worker-machine-count=1 \
  > capi-simod.yaml
kubectl apply -f capi-simod.yaml

kubectl get cluster  # verify the cluster is up
clusterctl describe cluster capi-simod  # cluster resources
kubectl get kubeadmcontrolplane  # verify the first control plane is up

# getting the cluster configuration
kind get kubeconfig --name capi-simod > capi-simod.kubeconfig

# deploying CNI solution
kubectl --kubeconfig=./capi-simod.kubeconfig apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/calico.yaml
kubectl --kubeconfig=./capi-simod.kubeconfig get nodes

# clean up
kubectl delete -f capi-simod.yaml
kubectl delete cluster capi-simod
kind delete cluster --name capi-simod
kind delete cluster
```

## Scaling and Autoscaling

https://cluster-api.sigs.k8s.io/tasks/automated-machine-management/autoscaling.html

```shell
kubectl get machinedeployment

# manual scaling
kubectl scale machinedeployment foo --replicas=3
```

Install cluster-autoscaler CLI tool from source, https://github.com/kubernetes/autoscaler:

```shell
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/cluster-autoscaler
git checkout cluster-autoscaler-1.26.1
go install .
cluster-autoscaler -h
```

```shell
export CAPI_VERSION=v1beta1
cluster-autoscaler --kubeconfig capi-simod.kubeconfig --cloud-provider=clusterapi --namespace=default --cluster-name=capi-simod --logtostderr --v=4

kubectl get machinedeployment
kubectl get machineset
kubectl get machine
kubectl get nodes
kubectl get pods -n kube-system
```
