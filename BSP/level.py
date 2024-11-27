from settings import *
import classes, random

sector1=classes.Area(20, 0, (127, 127, 127), (127, 127, 127), [], 0.2)
sector1.walls = [
    classes.Segment(0, 0, -4, 0, True, 5, True, 5, 0, 0, RED, 'tile000', 'tile092', 'tile092', 4, 4),

    classes.Segment(-4, 0, -8, 4, True, 1, True, 1, 5, 5, RED, 'tile000', 'tile092', 'tile092', 4, 4),

    classes.Segment(4, 4, 0, 0, False, None, False, None, 0, 0, RED, 'tile000', 'tile092', 'tile092', 4, 4),
    classes.Segment(-8, 4, -8, 8, False, None, False, None, 0, 0, RED, 'tile000', 'tile092', 'tile092', 4, 4),
    classes.Segment(-8, 8, -4, 12, False, None, False, None, 0, 0, RED, 'tile000', 'tile092', 'tile092', 4, 4),
    classes.Segment(-4, 12, 0, 12, False, None, False, None, 0, 0, RED, 'tile000', 'tile092', 'tile092', 4, 4),
    classes.Segment(0, 12, 4, 8, False, None, False, None, 0, 0, RED, 'tile000', 'tile092', 'tile092', 4, 4),
    classes.Segment(4, 8, 4, 4, False, None, False, None, 0, 0, RED, 'tile000', 'tile092', 'tile092', 4, 4),
]
sector2=classes.Area(20, 5, (127, 127, 127), (127, 127, 127), [], 0.8)
sector2.walls = [
    classes.Segment(-8, 4, -4, 0, True, 0, True, 0, 0, 10, RED, 'tile122', 'tile112', 'tile128', 4, 4),

    classes.Segment(-16, 4, -8, 4, False, None, False, None, 0, 0, RED, 'tile122', 'tile112', 'tile128', 4, 4),
    classes.Segment(-4, 0, -16, 0, False, None, False, None, 0, 0, RED, 'tile122', 'tile112', 'tile128', 4, 4),
    classes.Segment(-16, 0, -16, 4, True, 2, True, 2, 0, 0, RED, 'tile122', 'tile112', 'tile128', 4, 4),
]

sector3=classes.Area(35, 5, (127, 127, 127), (127, 127, 127), [], 0.8)
sector3.walls = [
    classes.Segment(-16, 4, -16, 0, True, 1, True, 1, 0, 15, RED, 'tile122', 'tile112', 'tile128', 4, 4),

    classes.Segment(-24, 0, -16, 4, False, None, False, None, 0, 0, RED, 'tile122', 'tile112', 'tile128', 4, 4),
    classes.Segment(-24, -8, -24, 0, False, None, False, None, 0, 0, RED, 'tile122', 'tile112', 'tile128', 4, 4),
    classes.Segment(-16, -8, -24, -8, False, None, False, None, 0, 0, RED, 'tile122', 'tile112', 'tile128', 4, 4),
    classes.Segment(-16, 0, -16, -4, False, None, False, None, 0, 0, RED, 'tile122', 'tile112', 'tile128', 4, 4),
    
    classes.Segment(-16, -4, -16, -8, True, 3, True, 3, 0, 15, RED, 'tile122', 'tile112', 'tile128', 4, 4),
]
sector4=classes.Area(30, 0, RED, RED, [], 1)
sector4.walls=[
    classes.Segment(-16, -8, -16, -4, True, 2, True, 2, 5, 5, RED, 'tile021', 'tile126', 'sky', 4, 4),
    classes.Segment(0, -8, -16, -8, False, None, False, None, 0, 0, RED, 'tile021', 'tile126', 'sky', 4, 4),
    classes.Segment(-16, -4, 0, -4, False, None, False, None, 0, 0, RED, 'tile021', 'tile126', 'sky', 4, 4),
    classes.Segment(0, -4, 0, -8, True, 4, True, 4, 0, 10, RED, 'tile021', 'tile126', 'sky', 4, 4),
]
sector5=classes.Area(20, 0, RED, RED, [], 0.8)
sector5.walls=[
    classes.Segment(0, -8, 0, -4, True, 3, True, 3, 0, 0, RED, 'tile132', 'tile133', 'tile139', 4, 4),
    classes.Segment(1, -8, 0, -8, False, None, False, None, 0, 0, RED, 'tile132', 'tile133', 'tile139', 4, 4),
    classes.Segment(0, -4, 1, -4, False, None, False, None, 0, 0, RED, 'tile132', 'tile133', 'tile139', 4, 4),
    classes.Segment(1, -4, 1, -8, False, None, False, None, 0, 0, RED, 'tile135', 'tile133', 'tile139', 4, 4),
]
sector6=classes.Area(20, 0, RED, RED, [], 0.8)
sector6.walls=[
    classes.Segment(-4, 0, 0, 0, True, 0, True, 0, 0, 0, RED, 'tile000', 'tile092', 'tile092', 4, 4),
    classes.Segment(-4, -4, -4, 0, False, None, False, None, 0, 0, RED, 'tile000', 'tile092', 'tile092', 4, 4),
    classes.Segment(0, 0, 0, -4, False, None, False, None, 0, 0, RED, 'tile000', 'tile092', 'tile092', 4, 4),
    classes.Segment(0, -4, -4, -4, True, 4, True, 4, 0, 0, RED, 'tile000', 'tile092', 'tile092', 4, 4),
]
sectors = [sector1, sector2, sector3, sector4, sector5, sector6]