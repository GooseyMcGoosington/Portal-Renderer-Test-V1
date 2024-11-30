from settings import *

@staticmethod
@njit
def transformVector(v, cs, sn):
    x, y = v
    tx = x*cs-y*sn
    ty = y*cs+x*sn
    return (tx, ty)

@staticmethod
@njit
def transformToScreen(f, v):
    x,y,z = v
    inv_y = 1 / y  # Avoid repeated division
    return (x * inv_y * f + W2, z * inv_y * f + H2)

@staticmethod
@njit
def transformYToScreen(f, v):
    _, y, z = v
    inv_y = 1 / y  # Avoid repeated division
    return z * inv_y * f + H2

# Yuriy Georgiev
@staticmethod
@njit
def clip(ax, ay, bx, by, px1, py1, px2, py2):
    a = (px1 - px2) * (ay - py2) - (py1 - py2) * (ax - px2)
    b = (py1 - py2) * (ax - bx) - (px1 - px2) * (ay - by)
    t = a / (b+1)
    ax -= t * (bx - ax)
    ay -= t * (by - ay)
    return ax, ay, t

@staticmethod
@njit
def rasterize_flat_wall(frame_buffer, x1, x2, y1, y2, y3, y4, c, clipping_bounds, render):
    def lerp(a, b, c):
        return (1 - a) * b + a * c
    dx = max(int((x2-x1)), 1)

    X1 = max(min(x1, W1), 1)
    X2 = max(min(x2, W1), 1)

    obstructed = False
    for x in prange(X1, X2):
        t = (x - x1) / dx
        Y1 = int(lerp(t, y1, y2))
        Y2 = int(lerp(t, y3, y4))
        for y in prange(Y1, Y2):
            if x > clipping_bounds[0] and x < clipping_bounds[1] and y > clipping_bounds[2] and y < clipping_bounds[3]:
                if (frame_buffer[x, y][0] == 0 and frame_buffer[x, y][1] == 0 and frame_buffer[x, y][0] == 0):
                    if render:
                        frame_buffer[x, y] = c
                    obstructed = False
    return obstructed
    
@staticmethod
@njit
def portal(frame_buffer, x1, x2, y1, y2, y3, y4, c, clipping_bounds, render):
    def lerp(a, b, c):
        return (1 - a) * b + a * c
    dx = max(int((x2-x1)), 1)

    X1 = max(min(x1, W1), 1)
    X2 = max(min(x2, W1), 1)

    obstructed = False
    full = False
    print(X2, X1)
    if abs(X2-X1) == 0:
        X1 = 1
        X2 = W1
        full = True
    
    for x in prange(X1, X2):
        if not full:
            t = (x - x1) / dx
            Y1 = int(lerp(t, y1, y2))
            Y2 = int(lerp(t, y3, y4))
        else:
            Y2 = 1
            Y1 = H1
        for y in prange(Y1, Y2):
            if x > clipping_bounds[0] and x < clipping_bounds[1] and y > clipping_bounds[2] and y < clipping_bounds[3]:
                if (frame_buffer[x, y][0] == 0 and frame_buffer[x, y][1] == 0 and frame_buffer[x, y][0] == 0):
                    if render:
                        frame_buffer[x, y] = c
                    obstructed = False
    return obstructed, full
    