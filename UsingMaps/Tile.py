import pygame
class Tile(object):
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.color = (0,0,0)
        self.hit = False
        self.height = 0
        self.animationTimer = 0
        self.animation = 0
        self.sprite = []
    
    def UpdateLoad(self, attr, value):
        ## sets color value
        if(attr == "color"):
            self.color = value
        ## sets hit value
        if(attr == "hit"):
            self.hit = value
        ## sets sprite list up
        ## needs updated to find out how many sprites
        if(attr == "sprite"):
            for i in range(0,2):
                self.sprite.append(pygame.image.load(value[:value.find("0")]+ str(i) + ".png"))

    def Update(self, dt):
        self.animationTimer += dt
        if(self.animationTimer >= .5):
            self.animation += 1
            self.animationTimer = 0
            if(self.animation >= len(self.sprite)):
                self.animation = 0



    def Hit(self, player):
        ## comes out with other tile types
        ## player.statuseffects.append(["DOT",2,2])
        return True
    
    def ResetHit(self):
        return True

    def Render(self, surface,xOffset,yOffset):
        if(len(self.sprite)):
            surface.blit(self.sprite[self.animation],(self.x + xOffset, self.y + yOffset))
        else:
            pygame.draw.rect(surface,self.color,(self.x + xOffset, self.y + yOffset, 32, 32))

    def __str__(self):
        if(self.hit):
            return "you can touch this"
        return "can't touch this"