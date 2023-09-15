# pi-traveler-backup
A hackathon project to turn your Raspberry into a standalone offline backup module. Never loose your precious travel photos again!

[![Project demo video](https://github.com/whiver/pi-traveler-backup/assets/394565/32cc5544-e8ec-4aa0-8dc4-3f6ab35d4fcd)](http://www.youtube.com/watch?v=9dVFOzRHLBg)

## How to use it
- Plug the USB drives that way:  
  ![Image describing the USB ports used for pi-traveler-backup](https://github.com/whiver/pi-traveler-backup/assets/394565/703e165d-7cfe-4fa4-95c7-405bdc4308a4)

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

![Raspberry GPIO reference](https://github.com/whiver/pi-traveler-backup/assets/394565/882da75c-ffa2-4dfb-9d3e-98e42fa484d6)


- Plug the LCD screen to the pins 1 (VCC),2 ,5 and 9 (GND)
- Plug the button to the pin 10 (RXD) and 1 (VCC)
- (Optional) The USB drives to use for the backup are hardcoded for the Raspberry Pi 3b. If you have another Raspberry Pi or want to change these ports, you'll need to update the devices to use in [`backup.sh`](https://github.com/whiver/pi-traveler-backup/blob/d52d24e5242958993a57fcc4b60bb6f3144560b3/backup.sh#L31-L32).
- 
### 2. Raspberry setup

1. Add Polkit permissions to mount the drive as user level : copy `10-udisk.pkla` from this project to `/etc/polkit-1/localauthority/50-local.d/10-udisks.pkla`  

   > ⚠️ This works only for old versions of Policy Kit which support only this config file format. This is the case as of today on current Raspbian images. If you see a folder `/etc/polkit-1/localauthority/` it means that it will also work for you. Otherwise, you need to use the Javascript format ([take a look here](https://github.com/coldfix/udiskie/wiki/Permissions)).

2. Setup the background service to launch on startup: copy `photo-backup.service` from this project to `/etc/systemd/system/photo-backup.service`
