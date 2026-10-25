variable "vpc_cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "CIDR for main VPC"
}

variable "azs" {
  type        = list(string)
  default     = ["eu-central-1a", "eu-central-1b"]
  description = "2 AZs for High-Availability"
}

variable "public_subnet_cidrs" {
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
  description = "CIDR for Public subnet (ALB)"
}

variable "private_app_subnet_cidrs" {
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
  description = "CIDR for Private App subnet (EKS / EC2)"
}

variable "private_data_subnet_cidrs" {
  type        = list(string)
  default     = ["10.0.20.0/24", "10.0.21.0/24"]
  description = "CIDR for Private Data subnet (RDS baza)"
}