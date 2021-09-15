
variable "vpc_cidr_block" {
   description = "Provide the CIDR block for VPC creation"
}


variable "vm_subnet_cidr" {
   description = "Provide the CIDR block for VM creation should be under VPC cidr block range"
}


variable "vpc_name" {
   description = "Name of the new VPC"
}



variable "region" {
   description = "region where we are going to deploy the resoouces ex:- us-east-1, us-west-1"
}

variable "ingress_rules" {
   description = "Traffic in coming ports which can be allowed"
}

variable "egress_rules" {
   description = "Traffic out going ports which can be allowed"
}
