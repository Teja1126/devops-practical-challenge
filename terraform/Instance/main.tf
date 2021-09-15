resource "aws_instance" "ec2" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  vpc_security_group_ids = var.sg_id
  subnet_id              = var.subnet_id
  key_name               = var.ssh_key_file

  root_block_device {
    volume_size = "20"
    volume_type = "standard"
  }

  tags = {
    Name = var.instance_name

  }
  volume_tags = {
    Name = join("-",[var.instance_name,"Volume"])
  }
}


output "instance_id" {
  value = aws_instance.ec2.id
}
