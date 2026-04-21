# GitOps Hub & Spoke Platform 🚀

A production-grade **Multi-Cluster GitOps Architecture** demonstration using **ArgoCD**, **Terraform**, and **Kubernetes**. This platform orchestrates application lifecycles from a central management "Hub" to distributed "Spoke" clusters (Staging & Production).

![Architecture Diagram](https://raw.githubusercontent.com/argoproj/argo-cd/master/docs/assets/argocd-architecture.png)
*(Note: Replace with your repository's workflow image after upload)*

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
└── scripts/            # Local lab setup scripts (Kind clusters)
```

## 🛠️ Local Demo Setup (Kind)

To replicate this environment locally on your machine:

1.  **Requirements**: `docker`, `kind`, `kubectl`, `helm`.
2.  **Spin up Clusters**:
    ```bash
    ./scripts/setup-kind.sh
    ```
    This script creates three clusters: `hub`, `spoke-staging`, and `spoke-prod`.
3.  **Bootstrap GitOps**:
    ```bash
    kubectl config use-context kind-hub
    kubectl apply -k gitops/hub/
    ```

## ☁️ Cloud Infrastructure (Terraform)

For production deployment on AWS:
```bash
cd terraform
terraform init
terraform apply
```

## 🤖 CI/CD Workflow

1.  **Code Change**: Developer pushes to `main`.
2.  **Build**: GitHub Image Builder kicks in, tags a new version.
3.  **Sync**: A second action updates `gitops/clusters/staging/values.yaml` with the new tag.
4.  **GitOps**: ArgoCD detects the change and reconciles the **Staging Spoke**.
5.  **Promote**: Manual PR merge to `prod` branch reconciles the **Production Spoke**.

---
*Created with ❤️ by Antigravity for your GitHub Portfolio.*
