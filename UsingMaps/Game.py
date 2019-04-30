import pygame
import time
from Player import Player
from Map import Map

class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800,608))
        self.StartGame()
        

    def StartGame(self):
        self.done = False
        self.map = Map("Map.txt")
        self.map.Load()
        self.player = Player(4*32,3*32,(400,304))
        self.starttime = time.time()
        self.lasttime = time.time()

    def GameLoop(self):
        while not self.done:
            self.starttime = time.time()
            self.screen.fill((0,0,0))

            events = pygame.event.get()

            # events list
            for e in events:
                if e.type == pygame.QUIT:
                    self.done = True
                if e.type == pygame.KEYDOWN:
                    if(e.key == pygame.K_RIGHT):
                        self.player.Movex(32)
                    if(e.key == pygame.K_LEFT):
                        self.player.Movex(-32)
                    if(e.key == pygame.K_DOWN):
                        self.player.Movey(32)
                    if(e.key == pygame.K_UP):
                        self.player.Movey(-32)

            self.map.CheckHit(self.player)

            self.map.Update(self.starttime - self.lasttime)
            ## not done
            self.map.Render(self.screen,(400-self.player.x,304-self.player.y))
            self.player.Render(self.screen)

            # Update Screen
            pygame.display.flip()
            self.lasttime = self.starttime

    def EndGame(self):
        pygame.display.quit()
        