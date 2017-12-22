from __future__ import print_function
from flask import Flask, render_template, request
#from xkcd_colors import xkcd_names_to_hex
import webcolors
import time
from random import randint

import socket
import array
import sys
from math import sin
import itertools

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

def look_up_color(name):
    try:
        color = webcolors.hex_to_rgb(xkcd_names_to_hex[name])
    except: # if we can't find a color, make up a random one
        color = [randint(0, 255), randint(0, 255), randint(0, 255)]
    return color

@public.route('/sms', methods=['POST'])
def parse_sms():
    message = str(request.form['Body']).strip().lower()
    print("Received text message: " + message)
    return ('<?xml version="1.0" encoding="UTF-8" ?><Response></Response>')

if __name__ == "__main__":
    public.run(host='0.0.0.0:5000', debug=True)
