import pygame, math, os, ctypes
import numpy as np
from numba import njit, prange
from pygame.math import Vector2 as vec2
import pygame.gfxdraw as gfx

W, H = 320, 200 ## 1920 x 1080 runs at 6 fps?? wow!! :D
W2, H2 = W/2, H/2
W1, H1 = W-1, H-1
screen_resolution = (W, H)

blankScreenArray = np.zeros((W, H, 3), dtype=np.uint8)
blank_portal_buffer = np.array([[False]*H]*W)

portal_buffer = blank_portal_buffer.copy()

ceiling_lut = [0]*W
floor_lut = [H1]*W

RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
TEAL=(0,255,255)
PINK=(255,0,255)

segTypes = {
    'IS_CEIL':2,
    'IS_FLOOR':1,
    'IS_WALL':0
}

sin=np.array([0.0]*360)
cos=np.array([0.0]*360)
for x in range(360):
    sin[x] = math.sin(x/180*math.pi)
    cos[x] = math.cos(x/180*math.pi)