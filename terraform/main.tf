module "vpc" {
  source = "./modules/vpc"

  project_name = "gitops-platform"
  environment  = "hub"
}

module "eks_hub" {
  source = "./modules/eks"

  cluster_name    = "hub-management"
  vpc_id          = module.vpc.vpc_id
  private_subnets = module.vpc.private_subnets
}

module "eks_staging" {
  source = "./modules/eks"

  cluster_name    = "spoke-staging"
  vpc_id          = module.vpc.vpc_id
  private_subnets = module.vpc.private_subnets
}

module "eks_prod" {
  source = "./modules/eks"

  cluster_name    = "spoke-prod"
  vpc_id          = module.vpc.vpc_id
  private_subnets = module.vpc.private_subnets
}

output "hub_endpoint" {
  value = module.eks_hub.cluster_endpoint
}
