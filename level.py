from settings import *
import classes, random

entities = []
s = 7
offset_x = -20*s
offset_y = -4*s
for x in range(10):
    entity_x = random.randint(-9, 9)+offset_x
    entity_y = random.randint(-9, 9)+offset_y

    entities.append(classes.Entity(entity_x, entity_y, 0, 0, 3, 16, 'box', 32, True))
    
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

sector3=classes.Area(35, 5, (127, 127, 127), (127, 127, 127), entities, 0.8)
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
"""
entity = classes.Entity(40, -60, 0, 0, 3, 16, 'box', 32, True)
sector1=classes.Area(20, 0, (127, 127, 127), (127, 127, 127), [entity], 0.5)
sector1.walls = [
    classes.Segment(0, 0, 0, 25, False, None, False, None, 0, 0, RED, 'tile000', 'tile092', 'sky', 4, 4),
    classes.Segment(0, 75, 0, 100, False, None, False, None, 0, 0, RED, 'tile000', 'tile092', 'sky', 4, 4),
    
    classes.Segment(-50, 75, 0, 75, False, None, False, None, 0, 0, RED, 'tile000', 'tile092', 'sky', 4, 4),
    classes.Segment(0, 25, -50, 25, False, None, False, None, 0, 0, RED, 'tile000', 'tile092', 'sky', 4, 4),
    classes.Segment(-50, 25, -50, 75, False, None, False, None, 0, 0, RED, 'tile000', 'tile092', 'sky', 4, 4),

    classes.Segment(0, 100, 100, 100, False, None, False, None, 0, 0, GREEN, 'tile000', 'tile092', 'sky', 4, 4),
    classes.Segment(100, 100, 100, 0, False, None, False, None, 0, 0, BLUE, 'tile000', 'tile092', 'sky', 4, 4),
    classes.Segment(100, 0, 60, 0, False, None, False, None, 0, 5, GREEN, 'tile000', 'tile092', 'sky', 4, 4), # def 1 leads into sector2, def2 leads into sector0
    classes.Segment(60, 0, 50, 0, True, 1, True, 1, 0, 5, GREEN, 'tile000', 'tile092', 'sky', 4, 4), # def 1 leads into sector2, def2 leads into sector0
    classes.Segment(50, 0, 40, 0, True, 1, True, 1, 0, 5, GREEN, 'tile000', 'tile092', 'sky', 4, 4), # def 1 leads into sector2, def2 leads into sector0
    classes.Segment(40, 0, 0, 0, False, None, False, None, 0, 5, GREEN, 'tile000', 'tile092', 'sky', 4, 4) # def 1 leads into sector2, def2 leads into sector0
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
]"""

## setup textures

## load textures
textures = {}

def init_textures():
    for file in os.listdir('textures'):
        texture = pygame.image.load(os.path.join('textures', file)).convert()
        texture_size = texture.get_size()
        array = pygame.surfarray.array3d(texture)
        name = os.path.splitext(file)[0]
        textures[name] = [array, texture_size, name]
    print(init_textures)
    for sector in sectors:
        lighting = sector.lighting
        for segment in sector.walls:
            segment.p1 = vec2(segment.p1.x*s, segment.p1.y*s)
            segment.p2 = vec2(segment.p2.x*s, segment.p2.y*s)
            # we will set the texture of the walls middle section, floor and ceiling
            segment.wall_texture = textures[segment.wall_texture].copy()
            segment.wall_texture[0] = (segment.wall_texture[0] * lighting).astype(np.uint8)

            segment.floor_texture = textures[segment.floor_texture].copy()
            segment.floor_texture[0] = (segment.floor_texture[0] * lighting).astype(np.uint8)

            segment.ceiling_texture = textures[segment.ceiling_texture].copy()
            segment.ceiling_texture[0] = (segment.ceiling_texture[0] * lighting).astype(np.uint8)