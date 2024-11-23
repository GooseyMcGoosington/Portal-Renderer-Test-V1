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
    x, y, z = v
    inv_y = 1 / y  # Avoid repeated division
    return (x * inv_y * f + W2, z * inv_y * f + H2)


@staticmethod
@njit
def transformYCoordToScreen(f, v):
    x, y, z = v
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
def rasterizeVisplane(screenArray, lut, texture, texture_scale, fov, f, yaw, cx, cy, elevation, is_sky, lighting, c):
    tanFOV=np.tan(fov/2)
    for x in prange(1, W1):
        Y = lut[x]
        if not is_sky:
            beta = x/W1*fov-fov/2
            alpha = (yaw+beta)
            cos_beta = np.cos(beta)
            sin_alpha = np.sin(alpha)
            cos_alpha = np.cos(alpha)
        else:
            angle = np.atan((x-W2)/W2*tanFOV)
            adjusted_angle = np.degrees(yaw + angle)
            texX = int(adjusted_angle/360*texture.shape[0])%texture.shape[0]
        
        direction = Y > H2
        if direction:
            for y in prange(Y, H1):
                if not (x > W1 or x < 1 or y > H1 or y < 1):
                    colAvg = (screenArray[x, y][0]+screenArray[x, y][1]+screenArray[x, y][2])/3
                    isFilled = colAvg > 0
                    if not isFilled:
                        if not is_sky:
                            r = abs(y-H2)
                            straightDist = (elevation*f)/r
                            d = (straightDist/cos_beta)
                            wx = cx + (sin_alpha*d)
                            wy = cy + (cos_alpha*d)

                            texX = int(wx*texture_scale)%texture.shape[0]
                            texY = int(wy*texture_scale)%texture.shape[1]

                            texture_clr = texture[texX, texY]
                            screenArray[x, y] = (texture_clr[0]*lighting, texture_clr[1]*lighting, texture_clr[2]*lighting)
                        else:
                            if y < texture.shape[1]:
                                texY = int(y)%texture.shape[1]
                                texture_col = texture[texX, texY]
                                texture_col = [
                                    max(texture_col[0], 0),
                                    max(texture_col[1], 0),
                                    max(texture_col[2], 0)
                                ]
                                screenArray[x, y] = texture_col
        else:
            for y in prange(1, Y):
                if not (x > W1 or x < 1 or y > H1 or y < 1):
                    colAvg = (screenArray[x, y][0]+screenArray[x, y][1]+screenArray[x, y][2])/3
                    isFilled = colAvg > 0
                    if not isFilled:
                        if not is_sky:
                            r = abs(y-H2)
                            straightDist = (elevation*f)/r
                            d = (straightDist/cos_beta)
                            wx = cx + (sin_alpha*d)
                            wy = cy + (cos_alpha*d)

                            texX = int(wx*texture_scale)%texture.shape[0]
                            texY = int(wy*texture_scale)%texture.shape[1]

                            texture_clr = texture[texX, texY]
                            screenArray[x, y] = (texture_clr[0]*lighting, texture_clr[1]*lighting, texture_clr[2]*lighting)
                        else:
                            if y < texture.shape[1]:
                                texY = int(y)%texture.shape[1]
                                texture_col = texture[texX, texY]
                                texture_col = [
                                    max(texture_col[0], 1),
                                    max(texture_col[1], 1),
                                    max(texture_col[2], 1)
                                ]
                                screenArray[x, y] = texture_col

@staticmethod
@njit
def is_portal_visible(screenArray, x0, x1, y0, y1, y2, y3):
    if x0 > x1:
        x1, x0 = x0, x1
        y1, y0, y3, y2 = y0, y1, y2, y3
    dyb = y1-y0
    dyt = y3-y2
    dx = max(x1-x0, 1)
    dyb_dx = dyb / dx
    dyt_dx = dyt / dx
    X0 = max(min(int(x0), W1), 1)
    X1 = max(min(int(x1), W1), 1)
    obstructed = True
    for x in prange(X0, X1):
        Y1 = int(dyb_dx * (x - x0) + y0)
        Y2 = int(dyt_dx * (x - x0) + y2)

        for y in prange(int(Y2), int(Y1)):
            if x > 1 and x < W1 and y > 1 and y < H1:
                colAvg = (screenArray[x, y][0]+screenArray[x, y][1]+screenArray[x, y][2])/3
                isFilled = colAvg > 0
                #screenArray[x, y] = (255, 0, 255)
                if not isFilled:
                    obstructed = False

    return obstructed

@staticmethod
@njit
def rasterize(screenArray, x0, x1, y0, y1, y2, y3, c, fill_Portal, portal_buffer, ceiling_lut, floor_lut, texture, wy0, wy1, t0, t1, wall_length, wall_height, is_sky, yaw, v_offset, lighting):
    ## cy is distance to camera

    def lerp(a, b, c):
        return (1-a)*b + a*c
    
    dyb = y1-y0
    dyt = y3-y2
    dx = max(x1-x0, 1)

    X0 = max(min(int(x0), W1), 1)
    X1 = max(min(int(x1), W1), 1)
    dyb_dx = dyb / dx
    dyt_dx = dyt / dx
    ## texture scaling
    sf = wall_length*0.1 # 20 units = repeats 0 times, 40 units = repeats once
    texLeft = lerp(t0, 0, sf)
    texRight = lerp(t1, 0, sf)

    for x in prange(int(X0), int(X1)):
        Y1 = int(dyb_dx * (x - x0) + y0)
        Y2 = int(dyt_dx * (x - x0) + y2)

        if not is_sky:
            ## textures X
            z0 = 1/wy0
            z1 = 1/wy1
            t = 0

            t = 1-(x-x0)/(x1-x0)
            
            top = (1-t)*(texLeft/z0)
            top += t*(texRight/z1)

            btm = (1-t)*wy0
            btm += t*wy1

            texX = (top/btm)*texture.shape[0]
            texX = int(texX)%texture.shape[0]
            ##
        else:
            angle = np.atan((x-W2)/W2*0.70020718322)
            adjusted_angle = yaw + np.degrees(angle)
            texX = int(adjusted_angle/360*texture.shape[0])%texture.shape[0]

        if int(Y2-Y1) == 0:
            ceiling_lut[x] = Y1
            floor_lut[x] = Y2

        for y in prange(int(Y2), int(Y1)):
            if not (x > W1 or x < 1 or y > H1 or y < 1):
                plane_Y1 = Y1
                plane_Y2 = Y2

                ceiling_lut[x] = plane_Y1
                floor_lut[x] = plane_Y2

                colAvg = (screenArray[x, y][0]+screenArray[x, y][1]+screenArray[x, y][2])/3
                isFilled = colAvg > 0
                if fill_Portal:
                    portal_buffer[x, y] = True
                else:
                    if not isFilled:
                        if not is_sky:
                            a = ((y-Y2)/(Y1-Y2))
                            v = lerp(a, 0, 1*wall_height*0.2)
                            texture_col = texture[texX, int(v*texture.shape[1]+v_offset)%texture.shape[1]]
                            screenArray[x, y] = (texture_col[0]*lighting, texture_col[1]*lighting, texture_col[2]*lighting)
                        else:
                            if y < texture.shape[1]:
                                texY = int(y)%texture.shape[1]
                                texture_col = texture[texX, texY]
                                screenArray[x, y] = texture_col
    return ceiling_lut, floor_lut

@staticmethod
@njit
def rasterizeSprite(screenArray, entity_x, entity_y, sprite, entity_depth, entity_scale, f):
    
    sprite_width = sprite.shape[0]
    sprite_height = sprite.shape[1]

    sprite_width_offset = sprite_width/2
    sprite_height_offset = sprite_height/2
    
    xStart = int(entity_x)
    xEnd = int(entity_x+(sprite_width/entity_depth*entity_scale))

    yStart = int(entity_y)
    yEnd = int(entity_y+(sprite_height/entity_depth*entity_scale))

    for x in prange(xStart, xEnd):
        for y in prange(yStart, yEnd):
            X = int(x - sprite_width_offset/entity_depth*entity_scale)
            Y = int(y - sprite_height_offset/entity_depth*entity_scale)
            if X > 1 and X < W1 and Y > 1 and Y < H1:
                pixel_col = (255, 0, 0)
                colAvg = (screenArray[X, Y][0]+screenArray[X, Y][1]+screenArray[X, Y][2])/3
                isFilled = colAvg > 0
                if not isFilled:
                    texX = int((x-xStart)*entity_depth/entity_scale)
                    texY = int((y-yStart)*entity_depth/entity_scale)

                    pixel_col = sprite[texX, texY]
                    screenArray[X, Y] = pixel_col

@staticmethod
@njit(parallel=True, fastmath=True, cache=True)
def resetScreenArray(screenArray):
    for x in prange(screenArray.shape[0]):
        for y in prange(screenArray.shape[1]):
            screenArray[x, y] = (0,0,0)
    return screenArray