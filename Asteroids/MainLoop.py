import time, random, math
import pygame
from PowerUp import PowerUp
from Ship import Ship
from Asteroids import Asteroid

def HitDetect(pos1,pos2,radius1, radius2):
    return math.sqrt((abs(pos1[0] - pos2[0]))*(abs(pos1[0] - pos2[0])) + (abs(pos1[1] - pos2[1]))*(abs(pos1[1] - pos2[1]))) < (radius1 + radius2)

# destroy asteroid and add to total
def DestroyAsteroid(asteroid, allAsteroids, powerups):
    if(type(asteroid) is Asteroid):
        if(asteroid.split > 1):
            for n in range(asteroid.pieces):                                             # TODO Semi working needs further work
                if((random.random() * 100) > 90):
                    powerups.append(PowerUp(asteroid.x,asteroid.y))
                else:
                    allAsteroids.append(Asteroid(asteroid.x,asteroid.y, asteroid.radius - (asteroid.radius/asteroid.split), 50 + random.random()* 25, random.random()*360, asteroid.split - 1, asteroid.pieces, asteroid.multi + 1))
        if(asteroid in allAsteroids):
            allAsteroids.remove(asteroid)

def ScreenWrap(ship, radius,screen):
    if(ship.x > (screen.get_width()+radius)):
        ship.x = -(radius - 1)
    if(ship.x < -radius):
        ship.x = screen.get_width() + radius - 1
    if(ship.y >  screen.get_height() + radius):
        ship.y = -(radius - 1)
    if(ship.y < -radius):
        ship.y = screen.get_height() + radius - 1

pygame.init()

screen = pygame.display.set_mode((800,600))

player = Ship(375,275, 11)

Points = 0

asteroids = []
powerups = []

for i in range(13):
    loaded = False
    while not loaded:
        x = random.random()*800
        y = random.random()*600
        if(not HitDetect((x,y), (player.x,player.y),20, 100)):
            loaded = True
    asteroids.append(Asteroid(x, y, 20, 50 + random.random()* 25, random.random()*360, 3, 4, 1))
moveL,moveR,moveU = (0,0,0)

lasttime = time.time()
thistime = time.time()
done = False

# Game Loop
while not done:
    thistime = time.time()
    dt = (thistime - lasttime)
    # Clear Screen
    screen.fill((0,0,0))

    events = pygame.event.get()

    # events list
    for e in events:
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                done = True
            if e.key == pygame.K_a:
                moveL = 1 #True
            if e.key == pygame.K_d:
                moveR = 1 #True
            if e.key == pygame.K_w:
                moveU = 1 #True
            if e.key == pygame.K_SPACE:
                player.FireBullet()
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_a:
                moveL = 0 #False
            if e.key == pygame.K_d:
                moveR = 0 #False
            if e.key == pygame.K_w:
                moveU = 0 #False
    # Movement
    if(moveL):
        player.direction += 1
    if(moveR):
        player.direction -= 1
    if(moveU):
        player.Addvel(dt)

    
    
    # Updates Position and anything else that is needed
    player.Update(dt)
    for p in powerups:
        if(HitDetect((player.x,player.y),(p.x,p.y), player.radius, 5)):
            powerups.remove(p)
            player.numBullets += 1
    for asteroid in asteroids:
        asteroid.update(dt)
        ScreenWrap(asteroid,asteroid.radius,screen)
        for b in player.bullets:
            if(HitDetect((b.x,b.y),(asteroid.x,asteroid.y),2,asteroid.radius)):
                Points += 100 * asteroid.multi
                DestroyAsteroid(asteroid, asteroids,powerups)
                player.bullets.remove(b)
                if(len(asteroids) == 0):
                    done = True
        if(HitDetect((player.x,player.y),(asteroid.x,asteroid.y), player.radius, asteroid.radius)):
            done = True
    ScreenWrap(player,player.radius,screen)
    


    # Render
    player.Render(screen)
    for asteroid in asteroids:
        asteroid.Render(screen)
    for p in powerups:
        p.Render(screen)
    # Update Screen
    pygame.display.flip()

    lasttime = thistime



font = pygame.font.SysFont("comicsonsms", 72)

text = font.render("Score: %d"% Points, True, (0,0,0))
while done:
    screen.fill((255,255,255))

    events = pygame.event.get()

    for e in events:
        if e.type == pygame.QUIT:
            done = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                done = False

    screen.blit(text, (400 - (text.get_width()/2),300 - (text.get_height()/2)))

    pygame.display.flip()


pygame.display.quit()