from settings import *
import classes, sys, level, BSP

## initialize
pygame.init()
pygame.mixer.init()

mainscreen = pygame.display.set_mode((W, H))

pygame.display.set_caption('Scotch Engine 1.0')

clock = pygame.time.Clock()
player = classes.Player(0, 0, 5, 6, 180, 70)
mainfont = pygame.font.SysFont(None, 48)
BSP_Partitioner = BSP.BSP(player, mainscreen)

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
    deltaTime = max(clock.tick(30), 1)
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
            pygame.image.save(mainscreen, 'screenshots\screenshot.jpg')
    else:
        screenshotHeld = False

    player.yaw %= 360
    player.yaw = max(player.yaw, 0)
    ## handle the engine stuff now
    s = 10
    pygame.draw.circle(mainscreen, (255, 255, 255), (player.x*s+W2, player.y*s+H2), 2, width=0)
    """pygame.draw.circle(mainscreen, (255, 255, 255), (player.x/s+W2, player.y/s+H2), 2, width=0)
    for sector in level.sectors:
        for wall in sector.walls:
            pygame.draw.line(mainscreen, (255, 0, 0), vec2(wall.p1.x/s, wall.p1.y/s) + vec2(W2, H2), vec2(wall.p2.x/s, wall.p2.y/s) + vec2(W2, H2), 1)
        for entity in sector.entities:
            pygame.draw.circle(mainscreen, (255, 0,0), (entity.x/s+W2, entity.y/s+H2), 2, width=0)"""
    pygame.draw.line(mainscreen, YELLOW, (player.x*s+W2, player.y*s+H2), ((player.x+np.sin(np.radians(player.yaw)+player.FOV/2)*64)*s+W2, (player.y+np.cos(np.radians(player.yaw)+player.FOV/2)*64)*s+H2), width=1)
    pygame.draw.line(mainscreen, YELLOW, (player.x*s+W2, player.y*s+H2), ((player.x+np.sin(np.radians(player.yaw)-player.FOV/2)*64)*s+W2, (player.y+np.cos(np.radians(player.yaw)-player.FOV/2)*64)*s+H2), width=1)
    BSP_Partitioner.traverse_node(BSP_Partitioner.root_node)
    pygame.display.update()
    mainscreen.fill(0)
    ## fps text
    pygame.display.set_caption(f'{clock.get_fps() :.1f}')
    avgFPS += clock.get_fps()
    avg += 1