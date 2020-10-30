# raspi-home-sensors

This repository contains code for a Raspberry Pi to monitor a home environment via sensors (e.g., hygrometer, thermometer) and write its data to a Google Sheet.

# Set up Google Sheets

## Set up Google Sheets API

This project uses a Google Sheet as a database for storing sensor data. In order to do so, we need to set up API access for Google Sheets. This requires creating a service account with Google Sheets API access which must belong to a Google Cloud project. The steps I took were below; adapt to your own use case as you see fit.

First, create a new [Google Cloud](console.cloud.google.com) project called `My Google Account`. This will serve as my gcloud project for managing API access for my personal Google Account and Drive data in general. (If you want to create a bespoke gcloud project for this use case, you can give a more specific name to your gcloud project.)

Then, enable the Google Sheets API for this gcloud project. The page to do this is called `APIs & Services` and can be found on the sidebar. The button with the text `Enable APIs and Services` will take you to another page where you can enable the Google Sheets API.

Next, create a service account. This can be done on the `APIs & Services > Credentials` page. I created a service account named `pi-sensors` and gave it a role of `Project > Editor`. 

Upon creation of this service account, Google will allow you to download access credentials for this account as a JSON file. This file will be copied to the Raspberry Pi in a later step.

## Set up Google Sheet 

After setting up a service account for interacting with the Sheets API, create a Google Sheet which will act as a database for this project. Name it whatever you want.

Then, share it with the service account's email and give it Editor permissions. The service account's email can be found in `client_secret.json` as the `client_email` field; alternatively, you can find it on Google Cloud on the `APIs & Services > Credentials` page.

# Setup Raspberry Pi

I've found that the most convenient way of using a raspi is through headless setup and operation. The instructions below document how to perform this headless setup with Raspberry Pi OS (formerly Raspbian).

## Install Raspberry Pi OS

First, write Raspberry Pi OS to a microSD card (I used Balena Etcher).

Then, navigate to the root of this card and create an empty file named `ssh`. This tells Raspberry Pi OS to enable SSH upon boot up.

Next, if your raspi supports wireless internet, you can tell it to automatically connect itself to a particular network by creating another file named `wpa_supplicant.conf` with the following contents:

```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
scan_ssid=1
ssid="your_wifi_ssid"
psk="your_wifi_password"
}
```

The microSD can now be inserted into the raspi.

## SSH in

Once the raspi is plugged in and it boots up, it should be possible to SSH into it using the command `ssh <192.168.LOCAL.IP> -l pi`. 

This IP can be determined by looking for the device named `raspberrypi` on your local network. You can use a network scanner or log into your router to list your devices. I would recommend logging into your router, since there's a good chance you'll also want to bind this device to a static IP.

## Add script

Next, we add our script to run every time the raspi starts up (i.e., is plugged in). To do so, edit `/etc/rc.local` with root permissions. Add the following line before `exit 0`:

```
until sudo python3 /sensor_loop.py >> /stdout.txt 2> /stderr.txt &
do
    echo "Sensor loop failed. Respawning script..."  >> /stdout.txt
    sleep 10
done
```

Note: The outer [until loop](https://linuxize.com/post/bash-until-loop/) scaffolding is a popular bash scripting pattern for restarting a program when it fails. Also, this redirects any program output into `stdout.txt` and `stderr.txt` files for ease of debugging. 

The `sensor_loop.py` file should then be copied from this repository into the `/` folder on the raspi:

```
scp /path/to/sensor_loop.py pi@192.168.LOCAL.IP:/sensor_loop.py
# (this command may not work outright because / is a protected directory, so use an intermediate directory and then sudo mv it to /)
```

Copy the URL of the Google Sheet used for this project into the global named `SHEET_URL`.

## Add service worker credentials

Copy the json file containing the service worker credentials to the `/` folder on the raspi and name it `client_secret.json`.

## Install python dependencies

```
sudo -H pip3 install gspread ntplib Adafruit_DHT
```

Note: `sudo -H` is necessary in order to install libraries globally (the `H` flag roughly means "don't install to the current user's home directory"). It's necessary to install libraries globally because the script is configured to run at boot up by root (root executes `rc.local`).
