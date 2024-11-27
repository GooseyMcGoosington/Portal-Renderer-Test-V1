from settings import *
import classes, level, engine

## initialize
pygame.init()

mainscreen = pygame.display.set_mode((W, H))

pygame.display.set_caption('Scotch Engine 1.0')

clock = pygame.time.Clock()
player = classes.Player(vec3(5, 50, 5), vec3(0, 0, 0), 0)
Engine = engine.Engine(player, mainscreen)
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
    deltaTime = max(clock.tick(60), 1)
    ## handle quit
    for event in pygame.event.get(): # User did something 
        if event.type == pygame.QUIT: # If user clicked close
            halt()
            break

    ## handle key input detection
    keyInput = pygame.key.get_pressed()
    yaw = math.radians(player.yaw)
    if keyInput[pygame.K_w]:
        player.position.x += 45*math.sin(yaw)/deltaTime
        player.position.y += 45*math.cos(yaw)/deltaTime
    if keyInput[pygame.K_s]:
        player.position.x -= 45*math.sin(yaw)/deltaTime
        player.position.y -= 45*math.cos(yaw)/deltaTime
    if keyInput[pygame.K_d]:
        player.yaw += 180/deltaTime
    if keyInput[pygame.K_a]:
        player.yaw -= 180/deltaTime
    if keyInput[pygame.K_x]:
        if not screenshotHeld:
            screenshotHeld = True
            pygame.image.save(mainscreen, 'screenshots\screenshot.jpg')
    else:
        screenshotHeld = False

    player.yaw = int(max(player.yaw%360, 0))
    ## handle the engine stuff now
    s = 1
    Engine.update()
    Engine.draw()
    for sector in level.sectors:
        for segment in sector.segments:
            pygame.draw.line(mainscreen, (255, 255, 255), segment.p1*s+OFFSET, segment.p2*s+OFFSET, width=1)
    pygame.display.update()
    mainscreen.fill(0)
    ## fps text
    pygame.display.set_caption(f'{clock.get_fps() :.1f}')
    avgFPS += clock.get_fps()
    avg += 1