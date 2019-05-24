import pygame

class Player(object):
    def __init__(self, x, y, screenPosition):
        self.x = x
        self.y = y
        self.nextx = x
        self.nexty = y
        self.screenLocation = screenPosition
        self.health = 100
        self.statuseffects = []
        self.quests = []
        self.done = False

    def Movex(self,amount):
        self.nextx = self.x + amount
    
    def Movey(self,amount):
        self.nexty = self.y + amount

    def Update(self,dt):
        removeDmgList = []
        removeQuestList = []
        for i in self.statuseffects:
            if(i[0] == "DOT"):
                i[1] -= dt
                self.health -= i[2] * dt
                if(i[1] <= 0 ):
                    removeDmgList.append(i)

        for i in self.quests:
            i[2] -= dt
            if(i[2] <= 0):
                removeQuestList.append(i)
        
        for i in removeQuestList:
            self.quests.remove(i)

        for i in removeDmgList:
            self.statuseffects.remove(i)


    def Render(self, surface):
        pygame.draw.rect(surface,(0,255,255),(self.screenLocation[0], self.screenLocation[1], 32, 32))
        pygame.draw.rect(surface, (255,0,0),(surface.get_width()/2, 0,self.health*2, 20))
        count = 0
        for i in self.quests:
            ## proper way is to have an initial time and do percentage over length
            pygame.draw.rect(surface,(255,211,0),(surface.get_width()/2, 21 + (21 * count), i[2]*10,20))