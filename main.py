from settings import *
from engine import Engine
import classes, sys, level, raster

## initialize
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Scotch Engine 1.0')

clock = pygame.time.Clock()
player = classes.Player(45, 45, 5, 6, 180, 70)

## load textures
textures = {}
sounds = {}

for file in os.listdir('textures'):
    texture = pygame.image.load(os.path.join('textures', file)).convert()
    texture_size = texture.get_size()
    array = pygame.surfarray.array3d(texture)
    name = os.path.splitext(file)[0]
    textures[name] = [array, texture_size]


Engine = Engine(player, screen, textures)
mainfont = pygame.font.SysFont(None, 48)

pygame.event.set_allowed([pygame.QUIT, pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_SPACE, pygame.K_x])

# special thanks to the following;
# https://www.reddit.com/user/Plus-Dust/ for their very generous help
# Yuriy Georgiev for their clipping function

screenshotHeld = False

avgFPS = 0
avg = 0
drawMap = False

def halt():
    print(round(avgFPS/avg, 1), ' was the average FPS this session')
    sys.exit()      
          
while True:
    deltaTime = max(clock.tick(), 1)
    ## handle quit
    for event in pygame.event.get(): # User did something 
        if event.type == pygame.QUIT: # If user clicked close
            halt()
            break

    ## handle key input detection
    keyInput = pygame.key.get_pressed()
    yaw = math.radians(player.yaw)
    if keyInput[pygame.K_w]:
        player.x += 45*math.sin(yaw)/deltaTime
        player.y += 45*math.cos(yaw)/deltaTime
    if keyInput[pygame.K_s]:
        player.x -= 45*math.sin(yaw)/deltaTime
        player.y -= 45*math.cos(yaw)/deltaTime
    if keyInput[pygame.K_d]:
        player.yaw += 180/deltaTime
    if keyInput[pygame.K_a]:
        player.yaw -= 180/deltaTime
    if keyInput[pygame.K_SPACE]:
        if not player.hasJumped:
            player.hasJumped = True
            player.jumpTick = pygame.time.get_ticks()
            player.vz += 3*deltaTime
    if keyInput[pygame.K_x]:
        if not screenshotHeld:
            screenshotHeld = True
            pygame.image.save(screen, 'screenshots\screenshot.jpg')
    else:
        screenshotHeld = False

    player.yaw %= 360
    player.yaw = max(player.yaw, 0)
    ## handle the engine stuff now
    if drawMap:
        s = 1.2
        for sector in level.sectors:
            for wall in sector.walls:
                pygame.draw.line(screen, (255, 0, 0), vec2(wall.p1.x/s, wall.p1.y/s) + vec2(W2, H2), vec2(wall.p2.x/s, wall.p2.y/s) + vec2(W2, H2), 1)
                # draw wall normal
                dy, dx = raster.get_segment_normal(wall.p1.x, wall.p1.y, wall.p2.x, wall.p2.y)
                normal = vec2(dy, dx)*4
                midpoint = (vec2(wall.p1.x, wall.p1.y) + vec2(wall.p2.x, wall.p2.y)) / 2 / s
                midpoint_screen = midpoint + vec2(W2, H2)

                normal_end = midpoint_screen+normal

                # Draw the normal as a line
                pygame.draw.line(screen, (0, 255, 0), midpoint_screen, normal_end, 1)  # Green line 

        pygame.display.update()
    else:
        Engine.update(deltaTime)
        Engine.draw()
    ## fps text
    pygame.display.set_caption(f'{clock.get_fps() :.1f}')
    avgFPS += clock.get_fps()
    avg += 1