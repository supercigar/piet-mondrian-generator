# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 16:13:35 2020

@author: Andreas
"""

from PIL import Image, ImageDraw
import numpy as np
import random

IMAGE_SIZE = (500, 500)
colors = [(255, 0,   0,   255), # Red
          (255, 0,   255, 255), # Magenta
          (255, 255, 0,   255), # Yellow
          (0,   255, 0,   255), # Green
          (0,   255, 255, 255), # Cyan
          (0,   0,   255, 255), # Blue
          (255, 255, 255, 255), # White
         ]
weights = [.1, .05, .05, .1, .05, .1, .55]

def generate_grid(im, n_lines, edge_margin=20):
    lines = []
    draw = ImageDraw.Draw(im)
    for i in range(n_lines):
        coords = [0,0,0,0]
        static = random.choice([0,1])
        coords[static] = coords[static+2] = random.randint(edge_margin,
                                                           IMAGE_SIZE[static] - edge_margin)
        coords[(static + 3) % 4] = IMAGE_SIZE[(static + 1) % 2]
        lines.append(coords)
    for line in lines:
        draw.line(line, fill=(0,0,0), width=random.randint(5, 10))
    return lines

def find_empty(im):
    array = np.array(im)[:,:,3] # Only get alpha value
    c = np.argmax(array == 0)
    return (int(c % IMAGE_SIZE[0]), int(c // IMAGE_SIZE[1]))

def fill(im, colors, weights):
    while True:
        color_number = np.random.choice(range(len(colors)), p=weights)
        ImageDraw.floodfill(im, find_empty(im), colors[color_number])
        if find_empty(im) == (0,0):
            return

im = Image.new("RGBA", IMAGE_SIZE, color=(255, 255, 255, 0))
lines = generate_grid(im, 5, 20)
fill(im, colors, weights)

im.save("piet.png")