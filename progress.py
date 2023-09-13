import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys

def readlines():
    line = []
    while True:
        c = sys.stdin.read(1)
        if (c == '\r') or (c == '\n'):
            yield ''.join(line)
            line = []
        elif c == '':
            # End of file reached
            if line:
                # Yield the last line if it's not empty
                yield ''.join(line)
            break
        else:
            line.append(c)

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

littlefont = font = ImageFont.truetype("Arial_Bold.ttf", 12, encoding="unic")
font = ImageFont.truetype("Arial_Bold.ttf", 16, encoding="unic") 

percentage = ""
photos = ""
for line in readlines():

    if " bytes/sec" in line or "total size is" in line:
        draw.text((x, top), text="Finished!", font=font, fill=255)
        draw.text((x, top+18), text="Contains " + str(photos.split('/')[1]) + " files", font=littlefont, fill=255)

    else:
        if "%" in line:
            percentage = line.split('%')[0][-2:]
            if percentage == "00":
                percentage = "100"
        if "to-chk=" in line:
            photos = line.split('to-chk=')[1][:-1]

        if percentage != "":
            draw.text((x, top), text="Status: " + str(percentage) + "%", font=font, fill=255)
        else:
            draw.text((x, top), text="Starting up...", font=font, fill=255)
        
        draw.text((x, top+22), text="Remains: " + str(photos), font=littlefont, fill=255)
        print(line)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(0.5)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
