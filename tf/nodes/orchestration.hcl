# Instantiate the orchestration module.

terraform {
  source = "../../../..//modules/infra/orchestration/"
}

locals {
  env              = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  ports            = local.env.locals.ports
  postgres_version = local.env.locals.postgres_version
  spot_provider    = "FARGATE_SPOT"
}

inputs = {
  capacity_providers = [local.spot_provider]
  default_capacity_provider_strategy = {
    base              = 1
    weight            = 100
    capacity_provider = local.spot_provider
  }
  opensearch_port  = local.ports.opensearch
  postgres_port    = local.ports.postgres
  postgres_version = local.postgres_version
  proxy_port       = local.ports.proxy
}
