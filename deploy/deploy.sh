#!/bin/bash

# Setup Minikube
minikube start
minikube addons enable ingress


# Deploy MongoDB Kubernetes operator
cd mongodb-kubernetes-operator/ || exit

kubectl apply -f deploy/clusterwide
kubectl apply -k config/rbac
kubectl apply -f config/crd/bases/mongodbcommunity.mongodb.com_mongodbcommunity.yaml
kubectl create -f config/manager/manager.yaml

kubectl rollout status deployment mongodb-kubernetes-operator


cd ../


# Deploy MongoDB Replica Set
kubectl apply -f mongodb-replicaset.yaml
kubectl apply -f mongodb-user-password-secret.yaml


# Deploy Document sample web app
kubectl apply -f document-web-app-deployment.yaml
kubectl rollout status deployment document-web-app

kubectl apply -f document-web-app-service.yaml


# Add NGINX Ingress object
kubectl apply -f nginx-ingress-class.yaml
kubectl apply -f nginx-ingress.yaml
