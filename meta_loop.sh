# 

until [ sudo python3 /sensor_loop.py >> /stdout.txt 2> /stderr.txt ]
do
    echo "Sensor loop failed. Respawning script..."  >> /stdout.txt
    sleep 10
done
