# trace-retarget

Cron to run the script 5 times every hour: 0,12,24,36,48 * * * * /bin/bash -l -c '/path/to/your/python_script.py >> /path/to/your/script.log 2>&1'
