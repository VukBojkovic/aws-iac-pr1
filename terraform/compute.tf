data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"]
}

resource "aws_launch_template" "app" {
  name_prefix   = "aws-iac-pr1-app-"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  vpc_security_group_ids = [aws_security_group.app_sg.id]

  # Dodeljujemo IAM profil instanci za pristup ECR-u
  iam_instance_profile {
    arn = aws_iam_instance_profile.ec2_profile.arn
  }

  user_data = base64encode(<<-EOF
              #!/bin/bash
              exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>&1)
              echo "Starting user_data script execution..."

              apt-get update -y
              apt-get install -y docker.io awscli python3-pip git

              systemctl start docker
              systemctl enable docker

              echo "Waiting for Docker daemon to start..."
              until docker info >/dev/null 2>&1; do
                sleep 2
              done

              echo "Logging in to Amazon ECR..."
              aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 804792415610.dkr.ecr.eu-central-1.amazonaws.com

              echo "Pulling Docker image..."
              docker pull 804792415610.dkr.ecr.eu-central-1.amazonaws.com/aws-iac-pr1-app:latest

              echo "Running Docker container with Database environment variables..."
              docker run -d --restart always -p 8080:8080 \
                -e DB_HOST="${aws_db_instance.database.address}" \
                -e DB_PORT="3306" \
                -e DB_USER="dbadmin" \
                -e DB_PASSWORD="LozinkaZaBazu123!" \
                -e DB_NAME="appdb" \
                804792415610.dkr.ecr.eu-central-1.amazonaws.com/aws-iac-pr1-app:latest
                
              echo "Container started successfully."
              EOF
  )

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name        = "aws-iac-pr1-app-node"
      Environment = "production"
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_autoscaling_group" "app_asg" {
  name_prefix         = "aws-iac-pr1-asg-"
  vpc_zone_identifier = aws_subnet.private_app[*].id

  min_size         = 2
  max_size         = 4
  desired_capacity = 2

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  target_group_arns = [aws_lb_target_group.app_tg.arn]

  health_check_type         = "ELB"
  health_check_grace_period = 300

  tag {
    key                 = "Name"
    value               = "aws-iac-pr1-asg-instance"
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_lb_target_group" "app_tg" {
  name     = "aws-iac-pr1-app-tg"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    protocol            = "HTTP"
    port                = "8080"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}


resource "aws_lb" "main" {
  name               = "aws-iac-pr1-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = aws_subnet.public[*].id

  tags = {
    Name = "aws-iac-pr1-alb"
  }
}


resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_tg.arn
  }
}