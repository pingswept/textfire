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

def look_up_style(name):
    if name == "fire":
        return 100
    if name == "ice":
        return 200
    else:
        return "Error: style"

def look_up_action(name):
    if name == "fade":
        return [5,4,3,2,1]
    if name == "wipe":
        return [0,0,1,1,1]
    else:
        return "Error: action"

p = parsley.makeGrammar("""
# [color][style][action][color][style][repeat:n][speed:n][duration:n]
# Parsley has a built-in rule, ws, to match whitespace.
#sequence = command+
#command = look ws+ action+ ws+ look+ repeat* speed* duration*
command = look:start ws action*:act ws look*:finish -> (start, act, finish)
action = ('fade'|'wipe'):a -> look_up_action(a)
# A "look" means a color displayed in a certain style.
look = color:c ws style:s -> (c, s)
color = ('blue'|'red'):c -> look_up_color(c)
style = ('fire'|'ice'):s -> look_up_style(s)
""", {
'look_up_color': look_up_color,
'look_up_style': look_up_style,
'look_up_action': look_up_action
},)

print p("blue fire fade red ice").command()