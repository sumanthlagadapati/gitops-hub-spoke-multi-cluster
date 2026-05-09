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

## 📊 Live Cluster Dashboard & Traffic Metrics

- Visit `/dashboard` on your Flask app to see live cluster status and traffic metrics (requests per route, cluster/environment info, etc).

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

## 🏛️ Architecture Design

### Overview

This platform uses a **Hub & Spoke Multi-Cluster GitOps Architecture** to manage and deploy applications securely and efficiently across multiple Kubernetes clusters. The architecture is designed for scalability, security, and operational transparency.

#### Components

- **Management Cluster (Hub):**
  - Runs ArgoCD for GitOps-based deployment management.
  - Uses ApplicationSets to automate deployment to all spoke clusters.
  - Integrates with Slack for real-time deployment notifications.
- **Spoke Clusters (Staging/Prod):**
  - Isolated Kubernetes clusters for different environments.
  - Each cluster receives deployments and updates from the Hub via ArgoCD ApplicationSets.
  - Supports dynamic scaling and independent upgrades.
- **CI/CD Pipeline:**
  - GitHub Actions automates Docker builds and Helm chart updates.
  - Auto-promotion mechanism updates Helm chart tags to trigger deployments.
- **Cloud Infrastructure:**
  - Terraform provisions EKS clusters and networking on AWS.
- **Flask Application:**
  - Provides a dashboard for cluster status and traffic metrics.
  - Implements secure user authentication, registration, and admin management.
  - All user/admin actions are audit-logged for security and compliance.

#### Security & User Management

- Passwords are securely hashed before storage.
- User registration and admin management are available via the Flask app.
- Audit logging tracks all login, logout, registration, and admin actions.
- Password reset functionality is implemented with secure, time-limited tokens.

#### Diagram

> **To add your architecture diagram:**
> 1. Add your architecture diagram image (e.g., `architecture.png`) to the project root or a `docs/images` folder.
> 2. Notify the maintainer or update the README to reference this image.
> 3. Would you like to:
>    - Upload an image file now (tell us the filename/path)?
>    - Use a specific external image URL?
>    - Have us create a placeholder diagram (ASCII or Mermaid) directly in the README?

Example (update the path as needed):
```markdown
![Architecture Diagram](docs/images/architecture.png)
```

*Created with ❤️ by [sumanthlagadapati](https://github.com/sumanthlagadapati).*
