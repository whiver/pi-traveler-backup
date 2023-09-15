# pi-traveler-backup
A hackathon project to turn your Raspberry into a standalone offline backup module. Never loose your precious travel photos again!

## Setup

### 0. Prerequisites

To run this project you need to have:
1. A Raspberry Pi (this projects runs on Raspberry Pi 3, but should be quite easily portable to other versions, the main difference being the mapping on the physical USB port used for input and for output)

2. A 128x32 LCD screen ([similar to this one](https://www.adafruit.com/product/931)) to display backup status

3. A push button ([such as this one](https://www.adafruit.com/product/367)) to start/stop the backup

4. 2 USB drives : 1 to be used as backup and 1 as data source

5. A bunch of wires!

### 1. Hardware wiring

We'll use this documentation page as a reference: https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio-and-the-40-pin-header

![Raspberry GPIO reference](image.png)

- Plug the LCD screen to the pins 1 (VCC),2 ,5 and 9 (GND)
- Plug the button to the pin 10 (RXD) and 1 (VCC)

### 2. Raspberry setup

1. Add Polkit permissions to mount the drive as user level : copy `10-udisk.pkla` from this project to `/etc/polkit-1/localauthority/50-local.d/10-udisks.pkla`  

   > ⚠️ This works only for old versions of Policy Kit which support only this config file format. This is the case as of today on current Raspbian images. If you see a folder `/etc/polkit-1/localauthority/` it means that it will also work for you. Otherwise, you need to use the Javascript format ([take a look here](https://github.com/coldfix/udiskie/wiki/Permissions)).

2. Setup the background service to launch on startup: copy `photo-backup.service` from this project to `/etc/systemd/system/photo-backup.service`

