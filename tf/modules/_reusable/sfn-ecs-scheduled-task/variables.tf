# Variables for the sfn-ecs-scheduled-task module.

variable "assign_public_ip" {
  description = "Should the step function be exposed."
  type        = bool
}

variable "aws_account" {
  description = "The AWS account where resources are created."
  type        = number
}

variable "aws_region" {
  description = "The AWS region where resources are created."
  type        = string
}

variable "backoff_rate" {
  description = "Multiplier that increases the retry interval on each attempt"
  type        = number
}

variable "container" {
  description = "The name of the task definition container."
  type        = string
}

variable "cluster" {
  description = "ARN identifying the ECS cluster."
  type        = string
}

variable "description" {
  description = "Information describing the purpose of this step function."
  type        = string
}

variable "ecs_task_role_arn" {
  description = "The ARN of the ECS task role."
  type        = string
}

variable "ecs_task_definition_arn" {
  description = "The ARN of the ECS task definition to be executed."
  type        = string
}

variable "ecs_task_execution_role_arn" {
  description = "The ARN of the ECS task execution role."
  type        = string
}

variable "environment" {
  description = "Identify the deployment environment."
  type        = string
}

variable "failure_sns_topic" {
  description = "SNS topic used to alert admins of task failures."
  type        = string
}

variable "heartbeat" {
  description = "How long between function 'heartbeats' before timeout (cannot exceed timeout)."
  type        = number
}

variable "kms_key_arn" {
  description = "ARN of thw KMS key to be used to encrypt the secret."
  type        = string
}

variable "max_attempts" {
  description = "Number of times to retry a failed function."
  type        = number
}

variable "launch_type" {
  description = "Defines the capacity the task will run on, eg. AWS Fargate."
  type        = string
}

variable "name" {
  description = "The name of the scheduled task."
  type        = string
}

variable "namespace" {
  description = "The project namespace."
  type        = string
}

variable "retry_interval" {
  description = "How long to wait between function retries."
  type        = number
}

variable "schedule_expression" {
  description = "The expression determining when the rule should run."
  type        = string
}

variable "security_groups" {
  description = "Security groups for the step function definition."
  type        = list(string)
}

variable "state" {
  description = "The state of the cloudwatch rule."
  type        = string
}

variable "subnets" {
  description = "Subnets for the step function definition."
  type        = list(string)
}

variable "timeout" {
  description = "The running time threshold for a function (must exceed heartbeat)."
  type        = number
}
