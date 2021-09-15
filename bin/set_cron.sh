cp ./nginx_status_check.py /opt/
{ crontab -l; echo "*/$1 * * * * python3 nginx_status_check.py"; } | crontab -

if [[ $? == 0 ]]; then
   echo "Cron job is set successfully"
fi
