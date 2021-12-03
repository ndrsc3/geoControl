# Project - GeoControl

## PinOut
https://pinout.xyz/#
- 2 5V Power -> LEDs + Switch
- 3 GPIO 2 LED - R
- 4 5V Power Relay
- 5 GPIO 3 LED - G
- 6 Ground Board
- 7 GPIO 4 LED B
- 8 GPIO 14 Relay 1


## Hardware
- Pi 3B
- 24V -> 5V Buck Regulator
- Sunfounder 2 Channel Relay w/ OptoCoupler https://www.sunfounder.com/products/2channel-relay-module

## Run at startup
- Add commad to .bashrc
    - sudo nano /home/pi/.bashrc