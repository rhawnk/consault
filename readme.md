# Helm umbrella chart for standing up a local/ephemeral (LOCAL DEVELOPMENT ONLY) consul/vault cluster

## Introduction

This projects lets you run a single node Consul/Vault cluster in 6 Kubernetes or minikube

## Contents

- [Motivation](#motivation)
- [Prerequisites](#prerequisites)
- [Build](#build)
- [Deploy](#deploy)
- [UI](#ui)
- [Vault](#vault)
- [Attributions](#attributions)

## Motivation

This project came out of a requirement to build ephemeral environments in Kubernetes, without impacting production data.  This also serves as a great local consul/vault endpoint for local development/testing

The workflow is:
- Edit the umbrella's values.yaml if needed
- Deploy the umbrella chart with helm
- Profit

## Prerequisites

- Minikube or Kubernetes
- Kubectl configured to talk to your Minikube or Kubernetes cluster
- Helm package manager

## Build

To Document process still

## Deploy

```bash
cd consault/charts-master/umbrella
<Edit values.yaml as needed>
helm dep up
helm install --name <NAME_THE_RELEASE> .
```

## UI

LoadBalanced vs NodePort for access to both consul/vault UIs via Kubernetes vs Minikube

## Vault

Vault runs as a dev server (DO NOT RUN THIS IN PRODUCTION), so it does not need to be initialized.
The Root and Unseal keys can be found in the logs, by running
```bash
kubectl logs <VAULT_POD_NAME> -c vault | awk '/Root Token/ { print $3 }'
```
Feel free to just set it as an env variable for reference.
```bash
ROOT_TOKEN=$(kubectl logs <VAULT_POD_NAME> -c vault | awk '/Root Token/ { print $3 }')
```

## Attributions

- [Consul helm chart](https://github.com/kubernetes/charts/tree/master/stable/consul)
- [Vault helm chart](https://github.com/kubernetes/charts/tree/master/incubator/vault)
- [Helm post install hook for WIP seed container](https://github.com/kubernetes/helm/blob/master/docs/examples/nginx/templates/post-install-job.yaml)
