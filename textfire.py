
import array
import colorsys
from dotstar import Adafruit_DotStar
from flask import Flask, render_template, request
from __future__ import print_function
import itertools
from math import sin
import parsley
from PIL import Image
from random import randint
import socket
import sys
import time
import webcolors
from xkcd_colors import xkcd_names_to_hex
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

def look_up_color(name):
    try:
        color = webcolors.hex_to_rgb(xkcd_names_to_hex[name])
    except: # if we can't find a color, make up a random one
        color = [randint(0, 255), randint(0, 255), randint(0, 255)]
    return color

p = parsley.makeGrammar("""
# [color][style][action][color][style][repeat:n][speed:n][duration:n]
#sequence = command+
#command = look ws+ action+ ws+ look+ repeat* speed* duration*
look = color:c (ws style:s -> 'COLOR' + ' ' + 'STYLE'
               | -> 'COLOR')
color = ('blue'|'red'):c -> look_up_color(c)
style = ('fire'|'ice'):s -> 'STYLE'
""", {'look_up_color': look_up_color})

wrapper = None

public = Flask(__name__)
public.config['PROPAGATE_EXCEPTIONS'] = True

# Include "no-cache" header in all POST responses
@public.after_request
def add_no_cache(response):
    if request.method == 'POST':
        response.cache_control.no_cache = True
    return response

### Home page ###
@public.route('/')
@public.route('/index.html')
def default_page():
    return render_template('/index.html')

def complement(color): # pass color as (r, g, b) tuple
    # simpler, slower version of http://stackoverflow.com/a/40234924
    return tuple(max(color) + min(color) - channel for channel in color)

@public.route('/sms', methods=['POST'])
def parse_sms():
    message = str(request.form['Body']).strip().lower()
    print("Received text message: " + message)
    return ('<?xml version="1.0" encoding="UTF-8" ?><Response></Response>')

if __name__ == "__main__":
    public.run(host='0.0.0.0:5000', debug=True)

# bring the fire

#while True:
#    for row in range(height):
#
#        hue_shift = 0.4
#        brightness = 1.0
#        duration = 1
#        for i in range(numpixels):
#            if(iterations > 0):
#                r, g, b = im.getpixel((i * spacing, row))
#            else:
#                r, g, b = (152, 48, 13) # assign average values of flames image
#            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
#            h = (h + hue_shift) % 1
#            v = v * brightness
#            r, g, b = colorsys.hsv_to_rgb(h, s, v)
#            pixels[i] = r*255.0, g*255.0, b*255.0
#            strip.setPixelColor(i, int(r*255.0), int(g*255.0), int(b*255.0))
#        strip.show()                     # Refresh strip
#    iterations = iterations - 1
