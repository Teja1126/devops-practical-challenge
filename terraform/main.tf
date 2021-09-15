terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
   region  = "us-west-1"
   profile = "default"
}


module "Network" {
  source = "/root/tmudraga/test-code/terraform/Network"

  vpc_name = "my-vpc"
  vpc_cidr_block = "10.0.0.0/16"

  region = "us-west-1"
  vm_subnet_cidr  = ["10.0.101.0/24"]

  ingress_rules = {"rule1"={"from_port"="22","to_port"="22","protocol"="tcp","cidr"=["10.0.0.0/16"]}, "rule2"={"from_port"="443","to_port"="443","protocol"="tcp","cidr"=["10.0.0.0/16"]}}
  egress_rules = {"rule1"={"from_port"="0","to_port"="0","protocol"="-1","cidr"=["0.0.0.0/0"]}}
}

output "op" {
  value = module.Network.my_sg_id
}

module "Instance" {
  source = "/root/tmudraga/test-code/terraform/Instance"

  instance_name = "test-instance"
  ami_id = "ami-xxxxxx"
  instance_type = "t2.micro"
  ssh_key_file  = "ec2-login" 
  sg_id  = [module.Network.my_sg_id]
  subnet_id = module.Network.my_subnet_id 
 
}

resource "local_file" "ec2_instances" {
  content = <<EOT
[nginx]
nginx ansible_host=module.Instance.instance_id
EOT

  filename = "../nginx.ini"
  depends_on = [module.Instance]
}
