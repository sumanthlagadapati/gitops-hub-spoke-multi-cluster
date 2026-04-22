# GitOps Hub & Spoke Platform 🚀

A production-grade **Multi-Cluster GitOps Architecture** demonstration using **ArgoCD**, **Terraform**, and **Kubernetes**. This platform orchestrates application lifecycles from a central management "Hub" to distributed "Spoke" clusters (Staging & Production).

![Architecture Diagram](https://raw.githubusercontent.com/sumanthlagadapati/gitops-hub-spoke-multi-cluster/main/README.md) # Placeholder for your image

## 🏗️ Platform Architecture

As depicted in the Hub & Spoke model, this setup consists of:

1.  **Management Cluster (Hub)**:
    *   **ArgoCD**: The GitOps engine watching the `gitops/` directory.
    *   **ApplicationSets**: Automatically generates application instances for every spoke cluster.
    *   **Slack Notifications**: Real-time alerts on sync failures or healthy deployments.
2.  **Spoke Clusters (Staging/Prod)**:
    *   Isolated environments for application workloads.
    *   Dynamic resource scaling via HPA.
3.  **CI/CD Pipeline**:
    *   **GitHub Actions**: Automates Docker builds and pushes to GHCR.
    *   **Auto-Promotion**: Updates Helm chart tags in the GitOps repo to trigger redeployments.

## 📁 Repository Structure

```tree
.
├── apps/               # Source code for microservices (Python/Flask)
├── charts/             # Helm charts for the platform
├── gitops/             # Source of truth for all Kubernetes resources
│   ├── hub/            # ArgoCD core installation & config
│   ├── notifications/  # Slack webhook & notification templates
│   └── clusters/       # Multi-cluster ApplicationSets definitions
├── terraform/          # AWS EKS & VPC Infrastructure-as-Code
└── scripts/            # Lab setup scripts (Kind clusters)
```

## 🛠️ Local Demo Setup (Kind)

To replicate this environment locally on your machine:

1.  **Requirements**: `docker`, `kind`, `kubectl`, `helm`.
2.  **Spin up Clusters**:
    - **Windows (PowerShell)**: `.\scripts\setup-kind.ps1`
    - **Linux/Mac (Bash)**: `./scripts/setup-kind.sh`
3.  **Bootstrap GitOps**:
    ```bash
    kubectl config use-context kind-hub
    kubectl apply -f gitops/clusters/appset-flask.yaml
    ```

## 🤖 GitHub Actions Setup

To enable the automated CI/CD pipeline:

1.  **Create Secret**: Go to your Repo **Settings > Secrets > Actions**.
2.  **Add `PAT_TOKEN`**: Generate a Personal Access Token with `repo` and `workflow` permissions and add it as a secret. This allows the CI to update your manifest files automatically.

## ☁️ Cloud Infrastructure (Terraform)

For production deployment on AWS:
```bash
cd terraform
terraform init
terraform apply
```

---
*Created with ❤️ by Antigravity for [sumanthlagadapati](https://github.com/sumanthlagadapati).*
