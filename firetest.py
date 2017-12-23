import colorsys
from dotstar import Adafruit_DotStar
from PIL import Image
import time

numpixels = 64 # Number of LEDs in strip
datapin  = 17
clockpin = 27
strip    = Adafruit_DotStar(numpixels, datapin, clockpin, 2500000)

strip.begin()           # Initialize pins for output
strip.setBrightness(64) # Limit brightness to ~1/4 duty cycle

gif_im = Image.open('embers-2015-04-14.gif')

im = gif_im.convert('RGB')

(width, height) = im.size
spacing = width / numpixels

pixels = [ (0,0,0) ] * numpixels

iterations = 1

while True:
    for row in range(height):

        hue_shift = 0.4 #readADC(0, 11, 9, 10, 8)
        brightness = 1.0 #readADC(1, 11, 9, 10, 8)
        duration = 1 #readADC(2, 11, 9, 10, 8)
        #print "duration: {0}".format(duration)
        for i in range(numpixels):
            # Flicker if blue button pressed, or red pressed recently
            if(iterations > 0):
                r, g, b = im.getpixel((i * spacing, row))
            else:
                r, g, b = (152, 48, 13) # assign average values of flames image
            # If yellow button pressed, stop flickering, even if in long period
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            h = (h + hue_shift) % 1
            v = v * brightness
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            pixels[i] = r*255.0, g*255.0, b*255.0
            strip.setPixelColor(i, int(r*255.0), int(g*255.0), int(b*255.0))
        strip.show()                     # Refresh strip
        #time.sleep(1.0 / 200)
        #print iterations
    iterations = iterations - 1



