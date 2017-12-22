import parsley
from random import randint
import webcolors
from xkcd_colors import xkcd_names_to_hex

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
#foo = 'a':one baz:two 'd'+ 'e' -> (one, two)
#baz = 'b' | 'c'
""", {'look_up_color': look_up_color})
