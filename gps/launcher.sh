#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd /home/pi/Documents/gps #where the script is
python3 gps.py #a commnad to run the script
cd /
