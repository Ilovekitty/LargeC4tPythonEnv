import pygame
import math

class Asteroid(object):
    def __init__(self, x, y, radius, speed, direction, split, pieces, multi):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.radius = radius
        self.color = (248,24,148)
        # number of splits
        self.split = split
        # number of chunks
        self.pieces = pieces
        self.multi = multi

    def update(self, dt):
        # where we move our asteroid
        self.x += math.cos(math.radians(-self.direction)) * self.speed * dt
        self.y += math.sin(math.radians(-self.direction)) * self.speed * dt

    def Render(self, surface):
        pygame.draw.circle(surface, self.color , (int(self.x),int(self.y)), int(self.radius), 1)