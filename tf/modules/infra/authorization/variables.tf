# Variables for the authorization module.

variable "allowed_oidc" {
  description = "Github repos/branches allowed to assume to OIDC role."
  type        = list(map(string))
}
