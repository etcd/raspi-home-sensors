# raspi-home-sensors

This repository contains code that enables any Raspberry Pi to regularly poll a DHT22 sensor for humidity and temperature and log the data to a Google Sheet. The code is lightweight and highly resilient against many types of failure. The code has multiple levels of failsafe and will restart operation automatically when it encounters errors (for example, whether internet connectivity goes out for 1 second or 1 year, the code will resume data transfer the moment internet connectivity is regained). The instructions also describe how to set up wireless connectivity on supported Raspberry Pis, so only one physical connection for power is necessary, enabling high portability for this project. 

# Set up Google Sheets

This project uses a Google Sheet as a database for storing sensor data.

## Set up Google Sheets API

First, we need to set up API access for Google Sheets. This requires creating a service account with Google Sheets API access which must belong to a Google Cloud project. The steps I took were below; adapt to your own use case as you see fit.

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

Once the raspi is plugged in and it boots up, it should automatically be possible to SSH into it using the command `ssh <192.168.LOCAL.IP> -l pi` (if not, you may be running into local network restrictions that need to be lifted). The default password for Raspberry Pi OS is `raspberry`. You should change the default password using `passwd`, as leaving the default is a security risk.

The IP of the raspi can be determined by looking for the device named `raspberrypi` on your local network. You can use a network scanner or log into your router to list your devices. Logging into your router is recommended, since there's a good chance you'll also want to assign a static IP to this device.

## Add scripts

Next, clone this repository to the raspi:

```
# clone to /home/pi
git clone https://github.com/etcd/raspi-home-sensors.git
```

Then, configure the code to run every time the raspi boots by editing `/etc/rc.local` with root permissions. Add the following line before `exit 0`:

```
/home/pi/raspi-home-sensors/code/meta_loop.sh &
```

The `meta_loop.sh` file (inside `code`) also needs to be made executable once cloned onto the raspi:

```
chmod +x meta_loop.sh
```

Finally, copy the URL of the Google Sheet into `meta_loop.sh` into the variable named `SHEET_URL`.

## Add service worker credentials

Copy the json file containing the service worker credentials to the raspi and name it `client_secret.json`. If this file is on your local computer, you can use SCP to copy it to the raspi:

```
scp /path/on/local/computer/client_secret.json pi@192.168.LOCAL.IP:/home/pi/raspi-home-sensors/code/client_secret.json
```

## Install dependencies

```
# Dependencies from apt
sudo apt-get install libgpiod2
# Dependencies from pip3
pip3 install gspread ntplib adafruit-circuitpython-dht netifaces
```
