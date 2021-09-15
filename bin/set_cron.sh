if [[ $# != 1 ]]; then
  echo "usage ./set_cron.sh <time_in_min>"
  echo "ex :- ./set_cron.sh 10"
  exit 1
fi

cp ./nginx_status_check.py /opt/
{ crontab -l; echo "*/$1 * * * * python3 nginx_status_check.py"; } | crontab -

if [[ $? == 0 ]]; then
   echo "Cron job is set successfully"
fi
