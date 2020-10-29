# raspi-home-sensors

This repository contains code for a Raspberry Pi to monitor a home environment via sensors (e.g., hygrometer, thermometer).

# Setup

I've found that the most convenient way of using a raspi is through headless setup and operation. The instructions below document how to perform this headless setup with Raspberry Pi OS (formerly Raspbian).

## Instal Raspberry Pi OS

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

## Add boot up script

Next, we add our script to run every time the raspi starts up (i.e., is plugged in). To do so, edit `/etc/rc.local` with root permissions. Add the following line before `exit 0`:

```
sudo python3 /home/pi/sensor_loop.py &
```

The `sensor_loop.py` file should then be copied from this repository into the `/home/pi/` folder on the raspi.

## Set up Google Sheets API

This project uses a Google Sheet as a database for storing sensor data. In order to do so, we need to set up API access for Google Sheets. [Here](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)'s the tutorial I used. Note: this requires creating a service account with Google Sheets API access which must belong to a Google Cloud project. In my case, I created this service account under a project called My Google Account as a project for managing API access to things related to my personal Google Account and Drive data.

## Install python dependencies

```
pip3 install gspread oauth2client
```
