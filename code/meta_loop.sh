#!/bin/bash

# THIS FILE IS EXECUTED BY ROOT.
# However, the command executed by this file is run by `pi`.
#
# Note: The [until loop](https://linuxize.com/post/bash-until-loop/) scaffolding
# is a popular bash scripting pattern for restarting a program when it fails.
# Also, this redirects any program output into `stdout.txt` and `stderr.txt` files
# for ease of debugging. 

# URL of Google Sheet
SHEET_URL='https://docs.google.com/spreadsheets/d/1WF35JEkQr129Cluj2MAp6fM3QjogUusoJytuiqaXZZs'

# Path where this script is located
CODE_PATH=`dirname "$0"`
# Path to log file for meta loop (this script)
META_LOG="${CODE_PATH}/meta_loop.log"
# Path to log file for sensor loop
SENSOR_LOG="${CODE_PATH}/sensor_loop.log"
# Path to Google client secret
SECRET_PATH="${CODE_PATH}/client_secret.json"
# Path to local sqlite database
LOCALDB_PATH="${CODE_PATH}/sensors.db"

# Counter for number of times until loop has run
counter=0

# Run meta_loop.sh as the user `pi`; respawns script upon failure
echo "------------------------------------------------------------" >>$META_LOG
echo "                    $(date +'%Y-%m-%d %H:%M:%S')            " >>$META_LOG
echo "                    Starting meta loop                      " >>$META_LOG
echo "------------------------------------------------------------" >>$META_LOG
until su pi -c "python3 ${CODE_PATH}/sensor_loop ${SECRET_PATH} ${SHEET_URL} ${LOCALDB_PATH}" >>$SENSOR_LOG 2>>$META_LOG
do
    echo "------------------------------------------------------------" >>$META_LOG
    echo "                    $(date +'%Y-%m-%d %H:%M:%S')            " >>$META_LOG
    echo "    Sensor loop failed critically (stderr output above).    " >>$META_LOG
    echo "           Failure count since restart: $counter.           " >>$META_LOG
    echo "                    Respawning script...                    " >>$META_LOG
    echo "------------------------------------------------------------" >>$META_LOG
    sleep 5
    ((counter++))
done

echo -e "\nSensor loop exited successfully, causing meta loop to exit successfully." >>$LOG_PATH
