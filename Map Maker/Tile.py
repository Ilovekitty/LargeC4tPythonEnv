import pygame
class Tile(object):
    def __init__(self, x, y, color, hit):
        self.x = x
        self.y = y
        self.color = color
        self.hit = hit
        self.height = 0
    
    def Render(self, surface,xOffset,yOffset):
        pygame.draw.rect(surface,self.color,(self.x + xOffset, self.y + yOffset, 16, 16))

    def __str__(self):
        if(self.hit):
            return "you can touch this"
        return "can't touch this"