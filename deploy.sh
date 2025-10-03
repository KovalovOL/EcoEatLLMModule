#!/bin/bash
set -e
set -o pipefail


eval $(minikube docker-env) 
docker build -t my-llm-service:latest .

kubectl apply -f k8s/
kubectl get pods