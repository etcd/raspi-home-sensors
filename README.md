# raspi-home-sensors

This repository contains code that enables a Raspberry Pi (Model 4 B, although other versions may work) to regularly poll a DHT22 sensor for humidity and temperature and log the data to a Google Sheet. The code is lightweight and highly resilient against many types of failure. The code has multiple levels of failsafe and will restart operation automatically when it encounters errors (for example, whether internet connectivity goes out for 1 second or 1 year, the code will resume data transfer the moment internet connectivity is regained).

Furthermore, since the Raspi Model 4 B comes with wireless integrated LAN, it only needs a single physical connection for power, enabling high portability for this project. 

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

Once the raspi is plugged in and it boots up, it should be possible to SSH into it using the command `ssh <192.168.LOCAL.IP> -l pi`. The default password for Raspberry Pi OS is `raspberry`. The login message should inform you to change the password using `passwd`, as leaving the default is a security risk.

This IP can be determined by looking for the device named `raspberrypi` on your local network. You can use a network scanner or log into your router to list your devices. I would recommend logging into your router, since there's a good chance you'll also want to bind this device to a static IP.

## Add scripts

Next, we configure our script to run every time the raspi starts up (i.e., is plugged in). To do so, edit `/etc/rc.local` with root permissions. Add the following line before `exit 0`:

```
/meta_loop.sh >> /stdout.txt 2> /stderr.txt &
```

The `meta_loop.sh` and `sensor_loop.py` files should then be copied from this repository into the `/` folder on the raspi:

```
scp /path/to/meta_loop.py pi@192.168.LOCAL.IP:/meta_loop.py
scp /path/to/sensor_loop.py pi@192.168.LOCAL.IP:/sensor_loop.py
# (this command may not work outright because / is a protected directory,
# so use an intermediate directory and then sudo mv it)
```

The `meta_loop.sh` file also needs to be made executable once moved onto the raspi:

```
chmod +x meta_loop.sh
```

Finally, copy the URL of the Google Sheet used for this project into the global named `SHEET_URL`.

## Add service worker credentials

Copy the json file containing the service worker credentials to the `/` folder on the raspi and name it `client_secret.json`.

## Install dependencies

```
# Dependencies from apt
sudo apt-get install libgpiod2
# Dependencies from pip3
sudo -H pip3 install gspread ntplib adafruit-circuitpython-dht
```

Note: `sudo -H` is necessary in order to install libraries globally (the `H` flag tells sudo to use the superuser's home directory). It's necessary to install libraries globally because the script is configured to run at boot time by root (root executes `rc.local`).
