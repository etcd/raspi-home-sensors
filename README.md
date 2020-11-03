# raspi-home-sensors

This repository contains code that enables any Raspberry Pi to regularly poll a DHT22 sensor for humidity and temperature and log the data to a Google Sheet. The code is lightweight and highly resilient against many types of failure. The code has multiple levels of failsafe and will restart operation automatically when it encounters errors (for example, whether internet connectivity goes out for 1 second or 1 year, the code will resume data transfer the moment internet connectivity is regained). The instructions also describe how to set up wireless connectivity on supported Raspberry Pis, so only one physical connection for power is necessary, enabling high portability for this project. 

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

## Install dependencies

```
# Dependencies from apt
sudo apt-get install libgpiod2
# Dependencies from pip3
pip3 install gspread ntplib adafruit-circuitpython-dht netifaces
```
