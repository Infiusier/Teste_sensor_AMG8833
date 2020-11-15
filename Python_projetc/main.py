import os,math,time

import numpy as np
import pygame
from scipy.interpolate import griddata
from colour import Color
import serial
import statistics
from Serial import Serial_Handle

pixels=[]
for i in range(64):
    pixels.append(30)


MINTEMP = 26

MAXTEMP = 32

COLORDEPTH = 1024

os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

height = 480
width = 480

blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))

colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

displayPixelWidth = width / 30
displayPixelHeight = height / 30

lcd = pygame.display.set_mode((width, height))
lcd.fill((255, 0, 0))

pygame.display.update()
pygame.mouse.set_visible(False)

lcd.fill((0, 0, 0))

pygame.display.update()

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def parse_thermal_array_input(pixels_input):
    try:
        pixels_output=pixels_input.split(',')
        del pixels_output[-1]
        
        
        for position in range(len(pixels_output)):
            
            pixels_output[position]=float(pixels_output[position])
            
            
        if len(pixels_output)==64:
            return pixels_output
        else:
            return pixels
    except:
        return pixels

serial_handle=Serial_Handle()
serial_handle.COM_Port='/dev/ttyUSB0'
print(serial_handle.serial_init())

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont("Arial", 25)

# render text



while True:
    result=serial_handle.read_from_serial()
    pixels = parse_thermal_array_input(result)
    #MAXTEMP=statistics.median(pixels)+20
    #MAXTEMP=constrain(MAXTEMP,0,80)
    
    label = myfont.render("Max temp: " + str(max(pixels)), 1, (0,0,0))
    
    
    pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
    bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
    
    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)],
            (displayPixelHeight * ix, displayPixelWidth * jx,
             displayPixelHeight, displayPixelWidth))

    
    lcd.blit(label, (0, 0))
    pygame.display.update()
















