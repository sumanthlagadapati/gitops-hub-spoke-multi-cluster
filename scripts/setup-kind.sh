#!/bin/bash

# Configuration
HUB_CLUSTER="hub"
STAGING_CLUSTER="spoke-staging"
PROD_CLUSTER="spoke-prod"

echo "🚀 Starting Hub & Spoke Local Lab Setup..."

# Create Hub Cluster
echo "📦 Creating Hub cluster..."
kind create cluster --name ${HUB_CLUSTER}

# Create Spoke Clusters
echo "📦 Creating Staging cluster..."
kind create cluster --name ${STAGING_CLUSTER}

echo "📦 Creating Production cluster..."
kind create cluster --name ${PROD_CLUSTER}

# Switch to Hub Context
echo "🔗 Switching to Hub context..."
kubectl config use-context kind-${HUB_CLUSTER}

# Install ArgoCD on Hub
echo "🔧 Installing ArgoCD on Hub cluster..."
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo "⏳ Waiting for ArgoCD pods to be ready..."
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s

echo "✅ Lab Setup Complete!"
echo "--------------------------------------------------"
echo "Management Hub: kind-${HUB_CLUSTER}"
echo "Staging Spoke:  kind-${STAGING_CLUSTER}"
echo "Production Spoke: kind-${PROD_CLUSTER}"
echo "--------------------------------------------------"
echo "Next Step: Register spoke clusters to the Hub."
