import pygame
class PowerUp(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def Render(self, surface):
        pygame.draw.circle(surface, (0, 255, 0),(int(self.x),int(self.y)), 5)