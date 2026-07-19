provider "aws" {
  region = "us-east-1"
}

resource "aws_db_instance" "billing_db" {
  allocated_storage    = 20
  engine               = "postgres"
  instance_class       = "db.t3.micro"
  db_name              = "billing_db"
  username             = "eaos"
  password             = "super-secret-password"
  skip_final_snapshot  = true
}
