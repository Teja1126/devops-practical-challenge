#!/bin/bash

sed -i -e "s+hosts: nginx+hosts: localhost+g" /main.yml
# Start the primary process 
ansible-playbook main.yml -b

# Start the helper process
tail -f /dev/null 
