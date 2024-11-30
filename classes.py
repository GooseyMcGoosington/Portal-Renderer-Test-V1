from settings import *
import engine

class Entity:
    def __init__(self, x, y, z, yaw, h, w, spriteName, scale, isTouchable):
        self.x=x
        self.y=y
        self.z=z

        self.vx=0
        self.vy=0
        self.vz=0

        self.yaw=yaw

        self.h=h
        self.w=w
        self.sprite=spriteName
        self.scale=scale

        self.isTouchable=isTouchable
        self.isBeingTouched=False
        
        
    def update(self, dt, engine, currentSector, listEntity):
        self.x+=self.vx*dt
        self.y+=self.vy*dt
        new_sector = engine.find_sector_from_point(self.x, self.y)
        if new_sector:
            self.z = new_sector.e
            if currentSector != new_sector: # we are definitely inside of a new sector
                current_self = currentSector.entities[currentSector.entities.index(listEntity)]
                currentSector.entities.remove(current_self)
                new_sector.entities.append(listEntity)
    def checkTouch(self, x, y, currentSector, listEntity):
        xLeft = self.x-self.w/2
        xRight = self.x+self.w/2
        yUp = self.y+self.w/2
        yDown = self.y-self.w/2

        touching = x > xLeft and x < xRight and y < yUp and y > yDown
        if touching: # you can only touch this once
            if not self.isBeingTouched:
                self.isBeingTouched = True
                currentSector.entities.remove(listEntity)
                print('Destroyed Entity')
                return
                # do stuff
        else:
            if self.isBeingTouched:
                self.isBeingTouched = False

class Player:
    def __init__(self, x, y, z, h, yaw, FOV):
        aspectRatio=W/H
        self.x=x
        self.y=y
        self.z=z
        self.vx=0
        self.vy=0
        self.vz=0
        self.h=h
        self.hasJumped=False
        self.jumpTick=0
        self.yaw=yaw
        self.FOVDegrees = FOV
        FOV=math.radians(FOV)
        self.FOV=FOV
        self.FocalLength=W/2/math.tan(FOV/2)
        self.viewWidth = math.tan(FOV/2) * 1
        self.fovWidthAtY = self.viewWidth*aspectRatio*0.9
        self.currentSector=None
        
class Segment:
    def __init__(self, x1, y1, x2, y2, def_1_portal, def_1_link, def_2_portal, def_2_link, portal_bottom, portal_top, c, wall_texture, floor_texture, ceiling_texture, floor_texture_scale, ceiling_texture_scale):
        self.p1 = vec2(x1, y1)
        self.p2 = vec2(x2, y2)
        self.def_1_portal=def_1_portal
        self.def_1_link=def_1_link
        self.def_2_portal=def_2_portal
        self.def_2_link=def_2_link
        self.portal_bottom=portal_bottom
        self.portal_top=portal_top 
        self.length=math.hypot(x2-x1, y2-y1)
        self.wall_texture=wall_texture
        self.floor_texture=floor_texture
        self.ceiling_texture=ceiling_texture
        self.floor_texture_scale=floor_texture_scale
        self.ceiling_texture_scale=ceiling_texture_scale
        self.c=c

class Area:
    def __init__(self, id, h, e, f_col, c_col, entities, lighting, lighting_effect):
        self.h=h
        self.e=e
        self.fc=f_col
        self.cc=c_col
        self.walls=[]
        self.entities=entities
        self.lighting=lighting
        self.lighting_effect=lighting_effect
        self.flicker_wait=0
        self.id=id