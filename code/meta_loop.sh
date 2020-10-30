#!/bin/bash

# THIS FILE IS EXECUTED BY ROOT.
# However, the command executed by this file is run by `pi`.
#
# Note: The [until loop](https://linuxize.com/post/bash-until-loop/) scaffolding
# is a popular bash scripting pattern for restarting a program when it fails.
# Also, this redirects any program output into `stdout.txt` and `stderr.txt` files
# for ease of debugging. 

# Path where this script is located
CODE_PATH=`dirname "$0"`
# Path to write meta loop logs to
LOG_PATH="${CODE_PATH}/meta_loop.log"

# Counter for number of times until loop has run
counter=0

# Run meta_loop.sh as the user `pi`; respawns script upon failure
echo "-----------------------------------" >>$LOG_PATH
echo "        Starting meta loop         " >>$LOG_PATH
echo "-----------------------------------" >>$LOG_PATH
until su pi -c "python3 ${CODE_PATH}/sensor_loop.py" >>/dev/null 2>>$LOG_PATH
do
    echo "------------------------------------------------------------" >>$LOG_PATH
    echo "    Sensor loop failed critically with the output above.    " >>$LOG_PATH
    echo "           Failure count since restart: $counter.           " >>$LOG_PATH
    echo "                    Respawning script...                    " >>$LOG_PATH
    echo "------------------------------------------------------------" >>$LOG_PATH
    sleep 5
    ((counter++))
done

echo -e "\nSensor loop exited successfully, causing meta loop to exit successfully." >>$LOG_PATH
