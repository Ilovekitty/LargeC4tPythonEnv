import pygame
import math

class bullet(object):
    def __init__(self,x,y,direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.radius = 2
    
    def Update(self, dt):
        self.x += math.cos(math.radians(-self.direction)) * 100 * dt
        self.y += math.sin(math.radians(-self.direction)) * 100 * dt

    def Render(self, surface):
        pygame.draw.circle(surface, (0,0,255), (int(self.x),int(self.y)), self.radius)

