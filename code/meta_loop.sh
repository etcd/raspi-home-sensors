#!/bin/bash

# THIS FILE IS EXECUTED BY ROOT.
# However, the command executed by this file is run by `pi`.
#
# Note: The [until loop](https://linuxize.com/post/bash-until-loop/) scaffolding
# is a popular bash scripting pattern for restarting a program when it fails.
# Also, this redirects any program output into `stdout.txt` and `stderr.txt` files
# for ease of debugging. 

# Path where this script is located
SCRIPT_PATH=`dirname "$0"`

# Counter for number of times until loop has run
counter=0

# Run meta_loop.sh as the user `pi`; respawns script upon failure
echo -e "Starting meta loop."
until su pi -c 'python3 sensor_loop.py'
do
    echo "Sensor loop failed (failure count since restart: $counter). Respawning script..."  >> "${SCRIPT_PATH}/meta_loop.log"
    sleep 5
    ((counter++))
done

echo -e "\nSensor loop exited successfully, causing meta loop to exit successfully."
