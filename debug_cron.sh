#!/bin/bash
echo "=== CRON DEBUG $(date) ===" >> /Users/shireen/Documents/trace-retarget/debug.log
echo "PATH: $PATH" >> /Users/shireen/Documents/trace-retarget/debug.log
echo "PWD: $(pwd)" >> /Users/shireen/Documents/trace-retarget/debug.log
echo "USER: $USER" >> /Users/shireen/Documents/trace-retarget/debug.log
echo "HOME: $HOME" >> /Users/shireen/Documents/trace-retarget/debug.log
echo "Python exists:" >> /Users/shireen/Documents/trace-retarget/debug.log
ls -la /Users/shireen/Documents/trace-retarget/ad-env/bin/python >> /Users/shireen/Documents/trace-retarget/debug.log 2>&1
echo "Script exists:" >> /Users/shireen/Documents/trace-retarget/debug.log
ls -la /Users/shireen/Documents/trace-retarget/data_sync/ads_snapshot_sync_to_s3.py >> /Users/shireen/Documents/trace-retarget/debug.log 2>&1
echo "Running script..." >> /Users/shireen/Documents/trace-retarget/debug.log
cd /Users/shireen/Documents/trace-retarget/data_sync
/Users/shireen/Documents/trace-retarget/ad-env/bin/python ads_snapshot_sync_to_s3.py >> /Users/shireen/Documents/trace-retarget/debug.log 2>&1
echo "Script completed with exit code: $?" >> /Users/shireen/Documents/trace-retarget/debug.log
echo "===================" >> /Users/shireen/Documents/trace-retarget/debug.log