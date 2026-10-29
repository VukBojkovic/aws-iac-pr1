resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "aws-iac-pr1-db-subnet-group"
  subnet_ids = aws_subnet.private_data[*].id

  tags = {
    Name = "aws-iac-pr1-db-subnet-group"
  }
}

resource "aws_db_instance" "database" {
  identifier            = "aws-iac-pr1-db"
  engine                = "mysql"
  engine_version        = "8.0"
  instance_class        = "db.t3.micro"
  allocated_storage     = 20
  max_allocated_storage = 50

  db_name  = "appdb"
  username = "dbadmin"
  password = "LozinkaZaBazu123!"

  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.db_sg.id]

  multi_az            = true
  skip_final_snapshot = true
  publicly_accessible = false

  tags = {
    Name = "aws-iac-pr1-rds"
  }
}