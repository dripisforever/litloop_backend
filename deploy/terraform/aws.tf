provider "aws" {
    region = "ap-south-1"
    profile = "dripta"
}

data "aws_vpc" "default_vpc" {
    default = true
}

data "aws_subnet_ids" "default_subnet" {
  vpc_id = data.aws_vpc.default_vpc.id
}

// Creating RSA key

variable "EC2_Key" {default="httpdserverkey"}
resource "tls_private_key" "httpdkey" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

// Creating AWS key-pair

resource "aws_key_pair" "generated_key" {
  key_name   = var.EC2_Key
  public_key = tls_private_key.httpdkey.public_key_openssh
}

// Creating security group for Instance

resource "aws_security_group" "httpd_security" {

depends_on = [
    aws_key_pair.generated_key,
  ]

  name         = "httpd-security"
  description  = "allow ssh and httpd"
  vpc_id       = data.aws_vpc.default_vpc.id

  ingress {
    description = "SSH Port"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "HTTPD Port"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "httpdsecurity"
  }
}

// Creating Security group for EFS

resource "aws_security_group" "efs_sg" {
  depends_on = [
    aws_security_group.httpd_security,
  ]
  name        = "httpd-efs-sg"
  description = "Security group for efs storage"
  vpc_id      = data.aws_vpc.default_vpc.id


  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.httpd_security.id]
  }
}
