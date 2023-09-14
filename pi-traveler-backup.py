import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import subprocess
import psutil
import os
import signal
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

running = False
pid = ""

RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()

def draw(first, second):
    global disp

    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    padding = -2
    top = padding
    font = ImageFont.truetype("Arial_Bold.ttf", 16, encoding="unic")
    littlefont = font = ImageFont.truetype("Arial_Bold.ttf", 12, encoding="unic")
    draw.text((0, top), text=first, font=font, fill=255)
    draw.text((0, top+18), text=second, font=littlefont, fill=255)
    disp.image(image)
    disp.display()

def button_callback(channel):
    global running
    global pid
    running = not(running)
    print("Button was pushed! " + str(running))

    if (running):
        instance = subprocess.Popen(["/home/hackathon/backup.sh"])
        pid = instance.pid
        draw("Starting up...", "Please wait...")
        
    else:
        draw("Stopping...", "Don't touch anything!")
        print("Let's kill " + str(pid))
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):  # or parent.children() for recursive=False
            os.kill(child.pid, signal.SIGTERM)
        os.kill(parent.pid, signal.SIGTERM)
        parent.wait()
        pid = ""
        draw("Copy stopped", "Press button to restart.")


#main 
draw("Hello :)", "Please press button.")

GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 15 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(15, GPIO.RISING, callback=button_callback, bouncetime=5000) # Setup event on pin 15 rising edge

while True:
    if pid != "":
        p = psutil.Process(pid)
        if p.status() == "zombie":
            p.wait()
            draw("Copy finished!", "Press to start again.")
            running = False
            pid = ""
    time.sleep(0.5)
