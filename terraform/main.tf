provider "aws" {
  region = "us-east-1"
}

# Security Group allowing HTTP (8080) and SSH (22)
resource "aws_security_group" "web_sg" {
  name        = "web-security-group"
  description = "Allow HTTP on 8080 and SSH"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
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

# # Key Pair
# resource "aws_key_pair" "deployer_key" {
#   key_name   = "deployer-key"
#   public_key = file("~/.ssh/id_rsa.pub")
# }

# EC2 Instance
resource "aws_instance" "web_server" {
  #ami             = "ami-0c55b159cbfafe1f0"
  ami             = "ami-05b10e08d247fb927"
  instance_type   = "t2.micro"
  key_name        = aws_key_pair.deployer_key.key_name
  security_groups = [aws_security_group.web_sg.name]

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install python3 -y
              sudo yum install pip -y
              sudo pip3 install flask
              echo "Python Environment Ready" > /home/ec2-user/ready.txt
              EOF

  tags = {
    Name = "PythonAppServer"
  }
}

# Output EC2 Public IP
output "public_ip" {
  value = aws_instance.web_server.public_ip
}
