# raspi-home-sensors

This repository contains code that enables a Raspberry Pi to regularly poll a DHT22 sensor for humidity and temperature and log the data to a database.

The code is lightweight and highly resilient against many types of failure. The code has multiple levels of failsafe and will restart operation automatically when it encounters errors (e.g., whether internet connectivity goes out for 1 second or 1 year, the code will resume data transfer the moment internet connectivity is regained).

# Set up Raspberry Pi

The instructions below document how to headlessly set up and run a Raspberry Pi.

## Install Raspberry Pi OS

1. Write Raspberry Pi OS Lite to a microSD card.

2. Navigate to the root of this card and create an empty file named `ssh`. This tells Raspberry Pi OS to start SSH upon every boot up.

3. If your raspi supports wireless internet, you can tell it to automatically connect itself to a particular network by creating another file named `wpa_supplicant.conf` with the following contents:

    ```
    country=US
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
    scan_ssid=1
    ssid="yOuR_WiFi_sSiD"
    psk="yOuR_WiFi_pAsSwOrD"
    }
    ```

    You can now insert the microSD card into the Raspberry Pi.

## First boot

1. Insert the microSD card into the Raspberry Pi and connect the Raspberry Pi to power.

2. Once the Pi boots up, you can SSH into it using the command `ssh <192.168.LOCAL.IP> -l pi`; the default password for Raspberry Pi OS is `raspberry`. You should change the default password using `passwd` as leaving the default is a security risk.

    You can determine your Raspberry Pi's IP by looking for the device named `raspberrypi` on your local network. You can use a network scanner or log into your router to list your devices. Logging into your router is recommended, since there's a good chance you'll also want to assign a static IP to this device.

4. Finally, if you're using the Lite version of Raspberry Pi OS, you will need to expand the filesystem and reboot:

    ```
    sudo raspi-config    # Select `Advanced Options` and then `Expand Filesystem`
    sudo reboot
    ```

## Install dependencies

```
# Ensure system is up to date
sudo apt-get update && sudo apt-get upgrade

# Install docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh


# Dependencies from apt
sudo apt-get install libgpiod2
# Dependencies from pip3
pip3 install gspread ntplib adafruit-circuitpython-dht netifaces
```

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
