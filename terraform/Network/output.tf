output "my_vpc_id" {
  value = aws_vpc.vpc.id
}

output "my_sg_id" {
  value = aws_security_group.vm_sg.id
}

output "my_subnet_id" {
  value = aws_subnet.subnet[0].id
}
