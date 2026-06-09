variable "region" {
  type    = string
  default = "ap-south-1"
}

variable "ami_id" {
  type    = string
}

variable "instance_type" {
  type    = string
}

variable "keypairs" {
  type    = string
  default = "awar08-kp"
}

variable "disable_api_stop" {
  type = bool
}

variable "environment" {
  type = string
}
