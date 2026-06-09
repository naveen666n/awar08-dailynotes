terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.49"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_instance" "webserver" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.keypairs
  disable_api_stop = var.disable_api_stop

  tags = {
    Name = var.environment
    Env   = var.environment
  }
}

