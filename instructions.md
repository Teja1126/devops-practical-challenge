# Assumptions
- Jenkins VM will have connactvity to AWS. [or Jankins VM alreay available AWS]
- aws configure should be ran already.
- Key [pem] is already available in AWS. [if this created from jenkins id_rsa.pub then passowrless login will be enabled]
- Key file is already available at Jenkins VM level.
- Ec2 instance going to create in private virtual cloud.
- Ec2 instance having public access. [public ip enabled] [below script we enabled igw, if only site accessable internal to VPC we can enable nat gw]

# EC2 instance Installation and nginx installtion 
## instructions
- Clone the repo "git clone <repo-url>"
- Make sure under /devops-practical-challenge/terraform/main.tf is updated with correct pem_key, ami_id and region, if profile is different we can set profile.
- Navigate to the bin directory "cd ./devops-practical-challenge/bin/"
- Run launcher.py file as showen in example "python3 launcher.py -a create -d test -k ello". [note:-  for now -k value is dummy we can pass any value will not be used inside code]
     -a option to create or destroy the resources
     -d option is deploymnet name using this we can deploy multiple environments like dev, test and automation etc.
- Above command will take 5 to 10 min to install the infra.
- Now navigate to the base directory "cd ../"
- Ran ansbile to install the nginx "ansible-playbook -b main.yml -i nginx.ini"
- Above command will take 2 to 4 min to install the nginx.
- now we can access the gui using url "http://<VM-ip>/test_html.html".
## setting cronjob.
  - Navigate to the bin directory "cd ./devops-practical-challenge/bin/"
  - Run ./set_cron.sh <time in min> [this can be run from where we want to monitor the nginx]
     ex :- ./set_cron.sh 10 [will set cron job to run every 10 min]
  

# Installing and setting Jenkins.
- Clone the repo "git clone <repo-url>"
- Navigate to the bin directory "cd ./devops-practical-challenge/".
- Run ansible playbook to install jenkins "ansible-playbook -b jenkins.yml" [we can use the same script to insatll jenkins in multiple VMs only we need to change hosts]
- Above command will take 5 to 10 min to install jenkins.
- Once jenkins installation is done Jenkins will prvide the otp. [make a note of this otp]
- Now we can access jenkins ui using url "http://<server_ip>:8080/jenkins/"
- Above url leads to autentication enter the copied otp. and install the required add-ons.
- Now jenkins is available.
- set Pipe line using the file Jenkins_pipline.txt under Jenkins_pipline "vim ./devops-practical-challenge/Jenkins_pipline/Jenkins_pipline.txt"
- Once pipeline set we can run the jenkins job by providing action, deployment, key permaters.
- this job will take approxmetly 10 min to set the infra as well as nginx installation.
  
 # Nginx in docker container.
- Clone the repo "git clone <repo-url>"
- Navigate to the bin directory "cd ./devops-practical-challenge/bin/".
- run the docker image generation script "./docker.sh <docker_image_name>"
- above command will take 10 min to create the docker image.
- we can use the same image to deploy nginx in k8s.
- we can satrt the container using command "docker run --expose 80 <docker_container_name> bash"
  
