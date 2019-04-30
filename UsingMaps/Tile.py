import pygame
class Tile(object):
    def __init__(self, x, y, color, hit,image):
        self.x = x
        self.y = y
        self.color = color
        self.hit = hit
        self.height = 0
        self.animationTimer = 0
        self.animation = 0
        self.sprite = []
        if(image): ## Fix and use the animation bool from load (animate amount for range)
            image[:image.find("0")]
            for i in range(0,2):
                self.sprite.append(pygame.image.load(image[:image.find("0")]+ str(i) + ".png"))
    
    def Update(self, dt):
        self.animationTimer += dt
        if(self.animationTimer >= .5):
            self.animation += 1
            self.animationTimer = 0
            if(self.animation >= len(self.sprite)):
                self.animation = 0



    def Hit(self, player):
        ## move dir and if a specific direction then move back
        if(player.lastx):
            player.x = player.lastx
        if(player.lasty):
            player.y = player.lasty
        
        player.lastx = 0
        player.lasty = 0

    def Render(self, surface,xOffset,yOffset):
        if(len(self.sprite)):
            surface.blit(self.sprite[self.animation],(self.x + xOffset, self.y + yOffset))
        else:
            pygame.draw.rect(surface,self.color,(self.x + xOffset, self.y + yOffset, 32, 32))

    def __str__(self):
        if(self.hit):
            return "you can touch this"
        return "can't touch this"