import pygame
import time
from Map import Map

## This the main file

somemap = Map("Map.txt")

somemap.Load()

pygame.init()

screen = pygame.display.set_mode((800,608))

done = False

# Game Loop
while not done:
    # Clear Screen
    screen.fill((0,0,0))

    events = pygame.event.get()

    # events list
    for e in events:
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.KEYDOWN:
            if(e.key == pygame.K_d):
                somemap.worldx += 16
            if(e.key == pygame.K_a):
                somemap.worldx -= 16
            if(e.key == pygame.K_s):
                somemap.worldy += 16
            if(e.key == pygame.K_w):
                somemap.worldy -= 16
        if e.type == pygame.KEYUP:
            if(e.key == pygame.K_d):
                somemap.worldx += 16
            if(e.key == pygame.K_a):
                somemap.worldx -= 16
            if(e.key == pygame.K_s):
                somemap.worldy += 16
            if(e.key == pygame.K_w):
                somemap.worldy -= 16

    somemap.Render(screen)

    # Update Screen
    pygame.display.flip()

pygame.display.quit()