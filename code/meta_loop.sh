#!/bin/bash

# THIS FILE IS EXECUTED BY ROOT.
# However, the command executed by this file is run by `pi`.
#
# Note: The [until loop](https://linuxize.com/post/bash-until-loop/) scaffolding
# is a popular bash scripting pattern for restarting a program when it fails.
# Also, this redirects any program output into `stdout.txt` and `stderr.txt` files
# for ease of debugging. 

counter=0

until su pi -c 'python3 sensor_loop.py >> stdout.txt 2> stderr.txt'
do
    echo "Sensor loop failed (failure count since restart: $counter). Respawning script..."  >> stdout.txt
    sleep 10
    ((counter++))
done