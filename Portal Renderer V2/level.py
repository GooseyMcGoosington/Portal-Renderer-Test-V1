from settings import *
import classes, random

sector1=classes.Sector(20, 0)
sector1.segments=[
    classes.Segment(vec2(0, 0), vec2(0, 100), False, 0, WALL, 0),
    classes.Segment(vec2(0, 100), vec2(100, 100), False, 0, WALL, 0),
    classes.Segment(vec2(100, 100), vec2(100, 0), True, 1, PORTAL, 1),
    classes.Segment(vec2(100, 0), vec2(20, 0), False, 1, WALL, 0),
    classes.Segment(vec2(20, 0), vec2(0, 0), True, 1, PORTAL, 2)
]

sector2=classes.Sector(20, 0)
sector2.segments=[
    classes.Segment(vec2(100, -100), vec2(100, -80), True, 2, PORTAL, 3),
    classes.Segment(vec2(100, -80), vec2(100, 0), False, 0, WALL, 0),

    classes.Segment(vec2(100, 0), vec2(100, 100), True, 0, PORTAL, 4),

    classes.Segment(vec2(100, 100), vec2(200, 100), False, 0, WALL, 0),
    classes.Segment(vec2(200, 100), vec2(200, -100), False, 0, WALL, 0),
    classes.Segment(vec2(200, -100), vec2(100, -100), False, 1, WALL, 0)
]

sector3=classes.Sector(20, 0)
sector3.segments=[
    classes.Segment(vec2(100, -100), vec2(100, -80), True, 1, PORTAL, 5),
    classes.Segment(vec2(100, -100), vec2(0, -100), False, 0, WALL, 0),
    classes.Segment(vec2(20, -80), vec2(100, -80), False, 0, WALL, 0),
    classes.Segment(vec2(0, -100), vec2(20, -80), True, 3, PORTAL, 6),
]
sector4=classes.Sector(20, 0)
sector4.segments=[
    classes.Segment(vec2(20, -80), vec2(0, -100), True, 2, PORTAL, 7),
    
    classes.Segment(vec2(20, 0), vec2(20, -80), False, 0, WALL, 0),
    classes.Segment(vec2(0, -100), vec2(0, 0), False, 0, WALL, 0),
    classes.Segment(vec2(0, 0), vec2(20, 0), True, 0, PORTAL, 8),
]
sectors=[sector1, sector2, sector3, sector4]