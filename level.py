from settings import *
import classes

entity = classes.Entity(40, -60, 0, 0, 3, 16, 'box', 32, True)
sector1=classes.Area(20, 0, (127, 127, 127), (127, 127, 127), [entity], 0.5)
sector1.walls = [
    classes.Segment(0, 0, 0, 100, False, None, False, None, 0, 0, RED, 'sky', 'tile032', 'sky', 4, 4),
    classes.Segment(0, 100, 100, 100, False, None, False, None, 0, 0, GREEN, 'sky', 'tile032', 'sky', 4, 4),
    classes.Segment(100, 100, 100, 0, False, None, False, None, 0, 0, BLUE, 'sky', 'tile032', 'sky', 4, 4),
    classes.Segment(100, 0, 60, 0, False, None, False, None, 0, 5, GREEN, 'tile021', 'tile032', 'sky', 4, 4), # def 1 leads into sector2, def2 leads into sector0
    classes.Segment(60, 0, 50, 0, True, 1, True, 1, 0, 5, GREEN, 'tile021', 'tile032', 'sky', 4, 4), # def 1 leads into sector2, def2 leads into sector0
    classes.Segment(50, 0, 40, 0, True, 1, True, 1, 0, 5, GREEN, 'tile021', 'tile032', 'sky', 4, 4), # def 1 leads into sector2, def2 leads into sector0
    classes.Segment(40, 0, 0, 0, False, None, False, None, 0, 5, GREEN, 'tile021', 'tile032', 'sky', 4, 4) # def 1 leads into sector2, def2 leads into sector0
]
sector2=classes.Area(20, 0, (127, 127, 127), (127, 127, 127), [], 1)
sector2.walls = [
    classes.Segment(60, 0, 60, -50, False, None, False, None, 0, 5, GREEN, 'tile021', 'tile032', 'tile139', 4, 4),
    classes.Segment(40, -50, 40, 0, False, None, False, None, 0, 5, GREEN, 'tile021', 'tile032', 'tile139', 4, 4),
    classes.Segment(60, -50, 40, -50, True, 2, True, 2, 5, 0, GREEN, 'tile021', 'tile032', 'tile139', 4, 4),
    classes.Segment(40, 0, 60, 0, True, 0, True, 0, 0, 5, GREEN, 'tile021', 'tile032', 'tile139', 4, 4)
]
sector3=classes.Area(20, 5, (127, 127, 127), (127, 127, 127), [], 1)
sector3.walls = [
    classes.Segment(40, -50, 60, -50, True, 1, True, 1, 0, 5, GREEN, 'tile065', 'tile004', 'tile139', 4, 4),
    classes.Segment(60, -50, 20, -90, False, None, False, None, 10, 5, GREEN, 'tile065', 'tile004', 'tile139', 4, 4),
    classes.Segment(20, -70, 40, -50, False, None, False, None, 10, 5, GREEN, 'tile065', 'tile004', 'tile139', 4, 4),
    classes.Segment(20, -90, 20, -70, True, 3, True, 3, 0, 0, GREEN, 'tile065', 'tile004', 'tile139', 4, 4),
]

sector4=classes.Area(20, 5, (127, 127, 127), (127, 127, 127), [], 0.5)
sector4.walls = [
    classes.Segment(20, -70, 20, -90, True, 2, True, 2, 0, 0, GREEN, 'tile099', 'tile098', 'tile099', 4, 4), # portal
    classes.Segment(20, -90, -60, -90, True, 4, True, 4, 5, 5, GREEN, 'tile068', 'tile098', 'tile099', 4, 4),
    classes.Segment(-60, -70, 20, -70, False, None, False, None, 0, 5, GREEN, 'tile099', 'tile098', 'tile099', 4, 4),
    classes.Segment(-60, -90, -60, -70, False, None, False, None, 0, 5, GREEN, 'tile099', 'tile098', 'tile099', 4, 4),

]

sector5=classes.Area(10, 10, (127, 127, 127), (127, 127, 127), [], 0.5)
sector5.walls = [
    classes.Segment(-60, -90, 20, -90, True, 3, True, 3, 0, 0, GREEN, 'tile068', 'tile085', 'tile085', 4, 4),
    classes.Segment(20, -90, 20, -110, False, None, False, None, 0, 5, GREEN, 'tile068', 'tile085', 'tile085', 4, 4),
    classes.Segment(-60, -110, -60, -90, False, None, False, None, 0, 5, GREEN, 'tile068', 'tile085', 'tile085', 4, 4),
    classes.Segment(20, -110, -60, -110, False, None, False, None, 0, 5, GREEN, 'tile068', 'tile085', 'tile085', 4, 4),
]

sectors = [sector1, sector2, sector3, sector4, sector5]