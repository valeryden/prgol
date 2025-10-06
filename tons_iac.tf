provider "aws" {
  region = "us-east-1"
}

# Insecure S3 bucket with public read access
resource "aws_s3_bucket" "public_bucket" {
  bucket = "highly-insecure-public-bucket"
}

resource "aws_s3_bucket_acl" "public_bucket_acl" {
  bucket = aws_s3_bucket.public_bucket.id
  acl    = "public-read"
}

resource "aws_s3_bucket_versioning" "public_bucket_versioning" {
  bucket = aws_s3_bucket.public_bucket.id
  versioning_configuration {
    status = "Disabled"
  }
}

# Insecure EC2 instance with public IP and SSH open to the world
resource "aws_instance" "public_instance" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  associate_public_ip_address = true
  
  root_block_device {
    encrypted = false
  }

  user_data = <<-EOF
    #!/bin/bash
    echo "AWS_SECRET_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE" > /etc/environment
    echo "AWS_ACCESS_KEY_ID=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" >> /etc/environment
  EOF
}

# Security group with everything open to the world
resource "aws_security_group" "wide_open_sg" {
  name        = "wide-open-security-group"
  description = "Allow all inbound and outbound traffic"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# RDS instance with publicly accessible and no encryption
resource "aws_db_instance" "public_db" {
  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "insecuredb"
  username             = "admin"
  password             = "password123"
  parameter_group_name = "default.mysql5.7"
  publicly_accessible  = true
  skip_final_snapshot  = true
  storage_encrypted    = false
}

# IAM user with admin access
resource "aws_iam_user" "admin_user" {
  name = "admin-user"
}

resource "aws_iam_user_policy" "admin_policy" {
  name = "admin-policy"
  user = aws_iam_user.admin_user.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "*",
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

# Unencrypted EBS volume
resource "aws_ebs_volume" "unencrypted_volume" {
  availability_zone = "us-east-1a"
  size              = 10
  encrypted         = false
}

# CloudTrail without encryption or log validation
resource "aws_cloudtrail" "insecure_trail" {
  name                          = "insecure-trail"
  s3_bucket_name                = aws_s3_bucket.public_bucket.id
  include_global_service_events = false
  enable_logging                = true
  enable_log_file_validation    = false
  kms_key_id                    = null
}

# SNS topic with no encryption
resource "aws_sns_topic" "unencrypted_topic" {
  name = "unencrypted-topic"
}

# Lambda function with excessive permissions
resource "aws_lambda_function" "insecure_lambda" {
  filename      = "lambda_function_payload.zip"
  function_name = "insecure_lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs12.x"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda_policy"
  role = aws_iam_role.lambda_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "*",
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

# API Gateway without WAF or proper authorization
resource "aws_api_gateway_rest_api" "insecure_api" {
  name        = "insecure-api"
  description = "Insecure API Gateway"
}

# DynamoDB table without encryption
resource "aws_dynamodb_table" "insecure_table" {
  name           = "insecure-table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }
}

# VPC without flow logs
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
}

# Default network ACL allowing all traffic
resource "aws_default_network_acl" "default" {
  default_network_acl_id = aws_vpc.main.default_network_acl_id

  ingress {
    protocol   = -1
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  egress {
    protocol   = -1
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }
}
