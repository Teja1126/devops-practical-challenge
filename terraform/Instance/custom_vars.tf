
variable "instance_name"{
  description = "Name of the EC2 instance"
}


variable "ami_id"{
  description = "Amazon Image id"
}

variable "instance_type"{
  description = "Type of the instance ex:- t2.micro, t2.medium"
}

variable "ssh_key_file"{
  description = "SSH key file which already created in aws will be used for SSH"
}

variable "sg_id"{
  description = "SSH key file which already created in aws will be used for SSH"
}

variable "subnet_id"{
  description = "SSH key file which already created in aws will be used for SSH"
}

