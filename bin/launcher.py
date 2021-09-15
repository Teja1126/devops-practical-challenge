'''
Usage:
    initiator.py  [(-a <action>)] [-d <deployment>] [(-k <rsa_keys>)]

    example-1 :   python3 initiator.py  -a 'create' -d 'SANDBOX' -a 'rsa-key'

    example-2 :   python3 initiator.py  -a 'destroy' -d 'SANDBOX' -a 'rsa-key'
'''

import os,sys
import time
import subprocess
from shutil import copyfile,copytree,rmtree
from docopt import docopt
import logging
import logging.handlers
from datetime import datetime



def set_logging():
 try:
    ## Getting current date.
    now = datetime.now()
    current_time = now.strftime("%d-%m-%Y-%H-%M-%S")

    ## Removing existing log file.
    response = subprocess.Popen("rm -rf /var/log/terraformInitiator*.log", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = response.communicate()

    ## creating new log file.
    logfilename = "/var/log/initiator"+current_time+".log"
    logging.basicConfig(filename=logfilename, filemode='w', level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s", datefmt='%m/%d/%Y %I:%M:%S')
    logging.addLevelName(logging.ERROR, 'INFRA_ERROR')

    ## Pshisng the loging to the console.
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.info("Logging started .... .... !!! ")
    return logfilename
 except Exception as e:
    logging.error("INFRA_ERROR: Exception occured While setting log file")
    logging.error(e)
    return False

def prepare_work_space(current_path, deployment_name, deployment_location, terraform_templets_location):
 ## This function is to prepare the workspace for terraform loaction.
 try:
    ## Verifying Deployment prest or not.
    if os.path.exists(deployment_location):
        logging.info("Deployment directory found !!! ... !!!")
        logging.info(" %s is present " %deployment_location)
    else:
        logging.info("No Deployment directory found hence Creating")
        logging.info(" %s is not present hence creating" %deployment_location)
        logging.info("Creating the %s" %(deployment_location))
        os.mkdir(deployment_location)

    logging.info(" Copying scripts from the %s resource to %s " %(terraform_templets_location, deployment_location))
    full_file_name = os.path.join(terraform_templets_location+'/', 'main.tf')
    if os.path.isfile(full_file_name):
        copyfile(full_file_name, deployment_location+'/main.tf')
        logging.info(" Copied %s to %s successfully " %(full_file_name, deployment_location))

    os.chdir(deployment_location)
 except Exception as e:
    logging.error("INFRA_ERROR: Exception occured While Setting work location")
    logging.error(e)
    return False

def planAndApply(deployment_name):
 try:
    logging.info("Calling terraform init")
    response = subprocess.Popen("terraform init", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, err = response.communicate()
    if (err != ''):
       logging.error(err)
       logging.error("INFRA_ERROR: terraform init failed")
       sys.exit(1)
    else:
       logging.info(out)
       logging.info("terraform init success")
    logging.info("Calling terraform plan to display the changes")
    response = subprocess.Popen("terraform plan", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, err = response.communicate()
    logging.info("terraform plan OUTPUT is ::::::::::::::::: ")
    if (err != ''):
       logging.error(err)
       logging.error("INFRA_ERROR: terraform plan failed")
       sys.exit(1)
    else:
       logging.info(out)
       logging.info("terraform plan success")

    logging.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! WARNNING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logging.info("!                                                                                         !")
    logging.info("!If terraform plan not ran manually and analyzed the plan oputput please terminate the job!")
    logging.info("!             Run the terraform plan first then run the create job                        !")
    logging.info("!                                                                                         !")
    logging.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    time_left(60)
    logging.info("Calling terraform apply")
    response = subprocess.Popen("terraform apply --auto-approve", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, err = response.communicate()
    if (err != ''):
       logging.error(err)
       logging.error("INFRA_ERROR: terraform apply failed")
       sys.exit(1)
    else:
       logging.info(out)
       logging.info("terraform apply success")
 except Exception as e:
    logging.error("INFRA_ERROR: Exception occured While applying the rsource")
    logging.error(e)
    return False

def destroy(deployment_name):
 try:
    response = subprocess.Popen("terraform init", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = response.communicate()
    response = subprocess.Popen("terraform destroy --auto-approve", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, err = response.communicate()
    if (err != ''):
       logging.error(err)
       logging.error("INFRA_ERROR: terraform destroy failed")
       sys.exit(1)
    else:
       logging.info(out)
       logging.info("terraform destroy success")
 except Exception as e:
    logging.error("INFRA_ERROR: Exception occured While destroying the rsource")
    logging.error(e)
    return False

def time_left(seconds):
    for x in range (int(seconds),0,-1):
        left = "Time left " + str(x) + "s"
        print (left, end="\r")
        time.sleep(1)



if __name__ == '__main__':
    try:

        ## Getting current directory.
        os.chdir("../")
        current_path = os.getcwd()

        logfilename = set_logging()

        logging.info("Starting initiator")
        logging.info("Deleted the log file under /var/log/")
        logging.info("new log file is created under /var/log/ is %s" %(logfilename))

        ## Parse the arguments
        args = docopt(__doc__)

        if args["-a"]:
            action = args["<action>"]

        if args["-k"]:
            key = args['<rsa_keys>']

        if args["-d"]:
            deployment_name = args['<deployment>']

        deployment_location=os.path.join("/opt/", deployment_name)
        terraform_templets_location=os.path.join(current_path, "terraform/")
        if (action == 'create'):
            prepare_work_space(current_path, deployment_name, deployment_location, terraform_templets_location)
            planAndApply(deployment_name)
        elif (action == 'destroy'):
            os.chdir(deployment_location)
            logging.info("Calling terraform destroy")
            destroy(deployment_name)
        else:
            logging.info("Selection %s is Wrong only support create and destroy" %action)
    except Exception as e:
        logging.error("INFRA_ERROR: Exception occured")
        logging.error(e)
        sys.exit(1)


