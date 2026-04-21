# GitOps Setup
$H = "hub"; $S = "spoke-staging"; $P = "spoke-prod"
Write-Output "🚀 Starting..."
if (!(Get-Command kind -ErrorAction SilentlyContinue)) { Write-Output "❌ No kind"; exit 1 }
kind create cluster --name $H
kind create cluster --name $S
kind create cluster --name $P
kubectl config use-context kind-$H
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s
Write-Output "✅ Done!"
