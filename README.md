# raspi-home-sensors

This repository contains code that enables a Raspberry Pi to regularly poll a DHT22 sensor for humidity and temperature and log the data to a database.

The code is lightweight and highly resilient against many types of failure. The code has multiple levels of failsafe and will restart operation automatically when it encounters errors (e.g., whether internet connectivity goes out for 1 second or 1 year, the code will resume data transfer the moment internet connectivity is regained).

# Set up Raspberry Pi

The instructions below document how to headlessly set up and run a Raspberry Pi.

## Install Raspberry Pi OS

1. Write Raspberry Pi OS Lite to a microSD card.

2. Navigate to the root of this card and create an empty file named `ssh`. This tells the Pi to start its SSH server upon every boot up.

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

4. Insert the microSD card into the Raspberry Pi.

## First boot

1. Connect the Raspberry Pi to power to turn it on.

2. Once the Pi boots up, you can SSH into it using the command `ssh <192.168.LOCAL.IP> -l pi` with the default password `raspberry`.

    NOTE: on Raspberry Pi OS Lite only, I've run into the issue where I cannot to SSH in upon first boot. Booting it a second time (I wait about a minute so that the first boot fully completes) fixes this problem.

3. Change the default password using `passwd` as leaving the default is a security risk.

4. Finally, if you're using the Lite version of Raspberry Pi OS, you may need to expand the filesystem and reboot:

    ```
    sudo raspi-config   # Select `Advanced Options` and then `Expand Filesystem`
    sudo reboot
    ```
    
    NOTE: I am unsure why I've needed to do this on some fresh installs and not others of the same Lite image on the same SD card to the same Pi. The command `df -h` tells you how much free space you have. If it doesn't say 100% used, then this is unnecessary.

## Install dependencies

1. Ensure the Pi is up to date (this can take a while, even with Raspberry Pi OS Lite):

    ``` 
    sudo apt update && sudo apt-get upgrade
    ```

2. Install Docker:

    ```
    # docker dependencies
    sudo apt install apt-transport-https ca-certificates software-properties-common
    ```
    
    ```
    # docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    ```

3. Install all other dependencies:
    ```
    sudo apt install libgpiod2
    pip3 install gspread ntplib adafruit-circuitpython-dht netifaces
    ```

## Add scripts

1. Clone this repository to the raspi:

    ```
    sudo apt install git    # since Lite doesn't come with git
    git clone https://github.com/etcd/raspi-home-sensors.git
    ```

2. Configure the code to run every time the raspi boots by editing `/etc/rc.local` with root permissions. Add the following line before `exit 0`:

    ```
    /home/pi/raspi-home-sensors/code/meta_loop.sh &
    ```

3. The `meta_loop.sh` file (inside `code`) also needs to be made executable once cloned onto the raspi:

    ```
    chmod +x meta_loop.sh
    ```

4. Finally, copy the URL of the Google Sheet into `meta_loop.sh` into the variable named `SHEET_URL`.
