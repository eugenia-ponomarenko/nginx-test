locals {
  region = "eu-central-1"
}

data "aws_ami" "ubuntu_24" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

data "aws_subnet" "default" {
  default_for_az = true
  availability_zone = "${local.region}a"
}

resource "aws_security_group" "nginx" {
  name        = "nginx-sg"
  description = "Allow HTTP and SSH access"
  vpc_id = data.aws_subnet.default.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
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
}

resource "aws_instance" "reverse_proxy" {
  ami             = data.aws_ami.ubuntu_24.id
  instance_type   = "t2.micro"
  key_name        = "test"
  security_groups = [aws_security_group.nginx.name]

  tags = {
    Name = "nginx-proxy"
  }
}

output "nginx_public_ip" {
  value = aws_instance.reverse_proxy.public_ip
}