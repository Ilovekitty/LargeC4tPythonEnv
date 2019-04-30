import pygame

class Player(object):
    def __init__(self, x, y, screenPosition):
        self.x = x
        self.y = y
        self.lastx = x
        self.lasty = y
        self.screenLocation = screenPosition

    def Movex(self,amount):
        self.lastx = self.x
        self.x += amount
    
    def Movey(self,amount):
        self.lasty = self.y
        self.y += amount

    def Render(self, surface):
        pygame.draw.rect(surface,(0,255,255),(self.screenLocation[0], self.screenLocation[1], 32, 32))