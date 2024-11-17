from settings import *
from engine import Engine
import classes, sys

## initialize
pygame.init()
pygame.mixer.init()

mainscreen = pygame.display.set_mode((1280, 720))
logical_screen = pygame.Surface((320, 200))
pygame.display.set_caption('Scotch Engine 1.0')

clock = pygame.time.Clock()
player = classes.Player(45, 45, 5, 6, 90, 70)

## load textures
textures = {}
sounds = {}

for file in os.listdir('textures'):
    texture = pygame.image.load(os.path.join('textures', file)).convert()
    texture_size = texture.get_size()
    array = pygame.surfarray.array3d(texture)
    name = os.path.splitext(file)[0]
    textures[name] = [array, texture_size]


Engine = Engine(player, logical_screen, mainscreen, textures)
mainfont = pygame.font.SysFont(None, 48)

pygame.event.set_allowed([pygame.QUIT, pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_SPACE, pygame.K_x])

# special thanks to the following;
# https://www.reddit.com/user/Plus-Dust/ for their very generous help
# Yuriy Georgiev for their clipping function

screenshotHeld = False

while True:
    deltaTime = 1/(1+clock.get_fps())
    ## handle quit
    for event in pygame.event.get(): # User did something 
        if event.type == pygame.QUIT: # If user clicked close
            sys.exit()            
            break
    ## handle key input detection
    keyInput = pygame.key.get_pressed()
    yaw = math.radians(player.yaw)
    if keyInput[pygame.K_w]:
        player.x += 45*math.sin(yaw)*deltaTime
        player.y += 45*math.cos(yaw)*deltaTime
    if keyInput[pygame.K_s]:
        player.x -= 45*math.sin(yaw)*deltaTime
        player.y -= 45*math.cos(yaw)*deltaTime
    if keyInput[pygame.K_d]:
        player.yaw += 180*deltaTime
    if keyInput[pygame.K_a]:
        player.yaw -= 180*deltaTime
    if keyInput[pygame.K_SPACE]:
        if not player.hasJumped:
            player.hasJumped = True
            player.jumpTick = pygame.time.get_ticks()
            player.vz += 5*9.82
    if keyInput[pygame.K_x]:
        if not screenshotHeld:
            screenshotHeld = True
            pygame.image.save(mainscreen, 'screenshots\screenshot.jpg')
    else:
        screenshotHeld = False

    player.yaw %= 360
    player.yaw = max(player.yaw, 0)
    ## handle the engine stuff now
    Engine.update(deltaTime)
    Engine.draw()
    """pygame.draw.circle(mainscreen, (255, 255, 255), (-player.x/2+W2, player.y/2+H2), 4)
    for sector in level.sectors:
        for wall in sector.walls:
            pygame.draw.line(mainscreen, (255, 0, 0), (-wall.x1/2+W2, wall.y1/2+H2), (-wall.x2/2+W2, wall.y2/2+H2), 1)"""
    ## fps text
    """fpstext = mainfont.render('FPS: ' + str(round(clock.get_fps())), False, (255, 255, 255))
    mainscreen.blit(fpstext, (0.5, 0.5))"""
    ## final
    clock.tick(30)
    
    pygame.display.update()
    