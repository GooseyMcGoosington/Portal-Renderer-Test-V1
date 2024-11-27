from settings import *

class Player:
    def __init__(self, position:vec3, velocity:vec3, yaw:int):
        self.position:vec3=position
        self.velocity:vec3=velocity
        self.yaw:int=yaw
        self.current_sector:Sector=None
        self.F=math.radians(90)
        self.f=W1/2/math.tan(self.F/2)

class Segment:
    def __init__(self, p1:vec2, p2:vec2, isPortal:bool, portalLink:int, c, portalID:int):
        self.p1:vec2=p1
        self.p2:vec2=p2
        self.isPortal=isPortal
        self.portalLink=portalLink
        self.c=c
        self.portalID=portalID

class Sector:
    def __init__(self, h:float, e:float):
        self.h:float=h
        self.e:float=e
        self.segments=[]