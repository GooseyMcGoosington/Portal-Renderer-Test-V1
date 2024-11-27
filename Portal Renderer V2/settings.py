import pygame, math, os, ctypes, sys
import numpy as np

from numba import njit, prange
from pygame.math import Vector2 as vec2
from pygame.math import Vector3 as vec3
import pygame.gfxdraw as gfx

W, H = 640, 480 ## 1920 x 1080 runs at 6 fps?? wow!! :D
W2, H2 = W/2, H/2
W1, H1 = W-1, H-1
OFFSET = vec2(W2, H2)
screen_resolution = (W, H)

frame_buffer = np.zeros((W, H, 3), dtype=np.uint8)

RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
TEAL=(0,255,255)
PINK=(255,0,255)
WALL=(200,200,200)
PORTAL=(200,0,0)

sin=np.array([0.0]*360)
cos=np.array([0.0]*360)
for x in range(360):
    sin[x] = math.sin(x/180*math.pi)
    cos[x] = math.cos(x/180*math.pi)