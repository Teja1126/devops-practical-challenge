data "aws_availability_zones" "available" {}

resource "aws_vpc" "vpc" {

  cidr_block       = var.vpc_cidr_block
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = var.vpc_name
  }
}


resource "aws_subnet" "subnet" {

  count = length(var.vm_subnet_cidr)
  vpc_id            = aws_vpc.vpc.id
  cidr_block = element(var.vm_subnet_cidr, count.index)
  availability_zone = element(data.aws_availability_zones.available.names, count.index)

  tags = {
    Name = join("-",["subnet", var.region])
  }
  map_public_ip_on_launch = true
}


resource "aws_internet_gateway" "igw" {

  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "igw"
  }
}

resource "aws_route_table" "route-table" {

  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "route_table"
  }
}


resource "aws_route_table_association" "rt_ass" {
  subnet_id      = aws_subnet.subnet[0].id
  route_table_id = aws_route_table.route-table.id

  depends_on = [aws_route_table.route-table]
}



resource "aws_security_group" "vm_sg" {
  name        = "vm-sg"
  description = "traffic rules"
  vpc_id      = aws_vpc.vpc.id

  tags = {
    Name = "vm-sg"
  }
}

resource "aws_security_group_rule" "sg_rules" {
  for_each = var.ingress_rules
  type              = "ingress"
  from_port         = each.value.from_port
  to_port           = each.value.to_port
  protocol          = each.value.protocol
  cidr_blocks       = each.value.cidr
  security_group_id = aws_security_group.vm_sg.id
}

resource "aws_security_group_rule" "sg_rules_egress" {
  for_each = var.egress_rules
  type              = "egress"
  from_port         = each.value.from_port
  to_port           = each.value.to_port
  protocol          = each.value.protocol
  cidr_blocks       = each.value.cidr
  security_group_id = aws_security_group.vm_sg.id
}

