# Inject the authorization module.

terraform {
  source = "../../../..//modules/infra/authorization/"
}

locals {
  env          = read_terragrunt_config(find_in_parent_folders("environment.hcl"))
  allowed_oidc = local.env.locals.allowed_oidc
}

inputs = {
  allowed_oidc = local.allowed_oidc
}
