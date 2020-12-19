#!/usr/bin/env python3

import mathpix
import json
import pyperclip
from pynput import mouse
import pyscreenshot as ImageGrab
from PIL import Image

r = []
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

position = []


def on_click(x, y, button, pressed):
    if pressed:
        position.append(x)
        position.append(y)
    else:
        position.append(x)
        position.append(y)
    if not pressed:
        return False


im = ImageGrab.grab()
while len(position) == 0:
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
bbox = (position[0], position[1], position[2], position[3])
print(bbox)
im.save('/tmp/latexTmp.jpg')
img = Image.open('/tmp/latexTmp.jpg')
cropped = img.crop(bbox)
cropped.save('/tmp/latexTmp.jpg')
try:
    r.append(
        mathpix.latex({
            'src': mathpix.image_uri('/tmp/latexTmp.jpg'),
            'formats': ['latex_simplified']
        }))
except:
    pass
r_new = []
for i in range(len(r)):
    try:
        islatexFormual = r[i]['latex_simplified'] != 0
        if (islatexFormual):
            r_new.append(r[i])
    except:
        pass

if (len(r_new) == 1):
    formatDict = {}
    formatDict['1'] = r_new[0]['latex_simplified']
    formatDict['2'] = '$' + r_new[0]['latex_simplified'] + '$'
    formatDict['3'] = '$$\n' + r_new[0]['latex_simplified'] + '\n$$'
    pyperclip.copy(formatDict[config["DEFAULT_FORMAT"]])
    spem = pyperclip.paste()
    print("Done!")
else:
    print("Error: Invalid Input Image!")
