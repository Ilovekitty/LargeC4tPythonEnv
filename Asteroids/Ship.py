import math
import pygame
from Bullets import bullet

class Ship(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.velx = 0
        self.vely = 0
        self.direction = 0
        self.radius = radius
        self.image = pygame.image.load("Ship.png")
        self.bullets = []
        self.numBullets = 1
    
    def FireBullet(self):
        if(self.numBullets > 1):
            angle = 35.0/(self.numBullets - 1)
            for i in range(self.numBullets):
                self.bullets.append(bullet(self.x,self.y,(self.direction -17.5) + angle * i - 1))
        else:
            self.bullets.append(bullet(self.x,self.y,self.direction))

    def Update(self,dt):
        
        for b in self.bullets:
            b.Update(dt)

        # This needs a fix to set the correct changes
        self.velx *= 1 - (0.2 * dt)
        self.vely *= 1 - (0.2 * dt)

        self.x += self.velx * dt
        self.y += self.vely * dt

    def Addvel(self,dt):
        # Limit the addition if it will go over max vel
        self.velx += math.cos(math.radians(-self.direction)) * 80 * dt
        self.vely += math.sin(math.radians(-self.direction)) * 80 * dt

    def Render(self, surface):
        orig_rect = self.image.get_rect()
        rot_image = pygame.transform.rotate(self.image, self.direction)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()

        for b in self.bullets:
            b.Render(surface)
            if(b.x > (surface.get_width()) 
                or (b.x < 0)
                or (b.y >  surface.get_height())
                or (b.y < 0)):
                self.bullets.remove(b)
            

        surface.blit(rot_image, (self.x-16,self.y-16))
        pygame.draw.circle(surface,(255,0,0),(int(self.x),int(self.y)),2)
