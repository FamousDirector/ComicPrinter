#!/bin/bash

set -e

sudo apt-get update
sudo apt-get install -y python3-pip libopenjp2-7 libtiff5 i2c-tools

python3 -m pip install -r requirements.txt

sudo raspi-config nonint do_i2c 0  # enable raspberrypi pins to do i2c