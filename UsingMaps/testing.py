import random

import os, sys
with open(os.devnull, 'w') as f:
    # disable stdout
    oldstdout = sys.stdout
    sys.stdout = f

    import pygame
    from pygame import *

    # enable stdout
    sys.stdout = oldstdout


import math # needs to be imported after pygames
import matplotlib.image as mpimg


import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
import time



class Simulation(gym.Env):

    # stuff for pygame or something
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    # should work hopefully on random generated rounds
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    # inits
    def __init__(self):

        # setup for the gameplay
        self.initialGameTime = 10
        self.gameTime        = 0
        self.highscore       =  0
        self.WHITE = (255, 255, 255)
        self.ORANGE = (255,140,0)
        self.GREEN = (100, 255, 100)
        self.BLACK = (0, 0, 0)
        self.WIDTH = 600
        self.HEIGHT = 400
        self.player = [0, 0]
        self.player_vel = 1.6
        self.score = 0
        self.enemies = []
        self.initial_enemies = 200
        self.area_in_each_direction = 400
        self.desired_pos = [self.WIDTH/2, self.HEIGHT/2]
        self.tickspeed = 60

        # pygame setup
        pygame.init()
        pygame.display.set_caption('Game')
        self.fps = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)

        # variables used by tensorflow, when accessing gym
        self.observation_space = np.array([self.WIDTH, self.HEIGHT, 3])
        self.action_space = spaces.Discrete(10)



    ## resets the game state and returns
    def reset(self):
        self.gameTime=self.initialGameTime

        self.enemies.clear()
        self.score = 0
        self.player = [self.WIDTH // 2, self.HEIGHT // 2]
        self.desired_pos = self.player

        for i in range(self.initial_enemies):
            self.enemies.append([
                random.randint(
                    self.WIDTH//2-self.area_in_each_direction,
                    self.WIDTH//2+self.area_in_each_direction),
                random.randint(
                    self.HEIGHT//2-self.area_in_each_direction,
                    self.HEIGHT//2+self.area_in_each_direction), 20])
        self.render()
        return self.getSS()


    # action gets passed (either number 0 - 9) or one hot encoded version
    # 0 does nothing, 9 makes agent stand ground, 1-8 moves directions
    def __handle_action(self, action):

        if isinstance(action, np.ndarray):
            action = np.argmax(action, axis=0)


        mx = self.WIDTH//2
        my = self.HEIGHT//2

        range = 20

        if(action==9):
            self.desired_pos = self.player
        if(action==0):
            return
        if(action==1):
            self.request_newpos([mx+range+range/2,my])
        if(action==2):
            self.request_newpos([mx-range-range/2,my])
        if(action==3):
            self.request_newpos([mx,my+range+range/2])
        if(action==4):
            self.request_newpos([mx,my-range-range/2])
        if(action==5):
            self.request_newpos([mx+range,my+range])
        if(action==6):
            self.request_newpos([mx+range,my-range])
        if(action==7):
            self.request_newpos([mx-range,my+range])
        if(action==8):
            self.request_newpos([mx-range,my-range])


    # makes the game update a step, according to action
    # takes input from handle_events() or the ML algo
    def step(self, action=0):

        done = False
        if(self.gameTime<=0):
            done = True
            return np.array(self.getSS()), self.score, done,{}

        self.__handle_action(action)

        self.handle_events()

        if(self.score>self.highscore):
            self.highscore = self.score

        self.gameTime -=0.015


        dist = math.hypot(self.desired_pos[0] - self.player[0],
                          self.desired_pos[1] - self.player[1])

        if(dist<2):
            self.desired_pos = self.player
        else:
            angle = math.atan2(self.player[1]-self.desired_pos[1],
                               self.player[0]-self.desired_pos[0])
            self.player[0]+= -self.player_vel * float(math.cos(angle))
            self.player[1]+= -self.player_vel * float(math.sin(angle))


        for enemy in self.enemies:

            enemy_dist = math.hypot(enemy[0] - self.player[0],
                              enemy[1] - self.player[1])

            #if(dist<2): # life should only be reduced when stand ground, but thats even harder
            if(enemy_dist<15):
                self.enemies.remove(enemy)
                if(enemy[2]<=0):
                    self.score +=1
                    #print(get_enemy_positions())
                else:
                    self.enemies.append([enemy[0],enemy[1],enemy[2]-1])

        return np.array(self.getSS()), self.score, done,{}




    # draws the individual things on the screen
    # (player, enemies, move indicator, points)
    def __draw(self):


        # if the env is closed forceably
        # self.screen.fill(self.BLACK) will trigger an error,
        # "pygame.error: display Surface quit" will be triggered,
        # but that should not be a problem for ML learning/testing
        self.screen.fill(self.BLACK)

        player = self.player
        gameTime = self.gameTime
        desired_pos = self.desired_pos
        score = self.score
        highscore = self.highscore

        pygame.draw.circle(self.screen, self.ORANGE, [self.WIDTH // 2, self.HEIGHT // 2], 15, 0)

        pygame.draw.circle(self.screen, self.WHITE, [int(desired_pos[0] - player[0] + self.WIDTH // 2), int(desired_pos[1] - player[1] + self.HEIGHT // 2)], 9, 0)

        for enemy in self.enemies:
            relative = self.__absolute_to_relative(enemy)
            pygame.draw.circle(self.screen, self.GREEN, relative, 10, 0)
            pygame.draw.line(self.screen, self.GREEN,
                             [relative[0]-11, relative[1]-15],
                             [relative[0]-11 +enemy[2], relative[1]-15],
                             4)
            pygame.draw.circle(self.screen, self.GREEN, relative, 10, 0)

        font = pygame.font.SysFont("Arial", 30)

        label1 = font.render("Time " + str(int(gameTime)), 1, (255, 255, 0))
        self.screen.blit(label1, (50, 15))

        label2 = font.render("Score " + str(score), 1, (255, 255, 0))
        self.screen.blit(label2, (440, 15))

        label2 = font.render("Highscore " + str(highscore), 1, (255, 255, 0))
        self.screen.blit(label2, (440, 45))


    # if you want to know (unused helper method)
    def __absolute_to_relative(self,enemy):
        absolute = [int(enemy[0]-self.player[0])+ self.WIDTH//2, int(enemy[1]-self.player[1])+ self.HEIGHT//2]
        return absolute

    # get all enemy positions [[x,y],[x,y]...] format
    # if you want to know them
    def get_enemy_positions(self):
        lst = []
        for enemy in self.enemies:
            lst.append(self.__absolute_to_relative(enemy))
        return lst


    #requesting a new position to walk to [x,y]
    def request_newpos(self, pos):

        self.desired_pos = [pos[0]  + self.player[0] - (self.WIDTH//2 ) ,
                            pos[1]  + self.player[1] - (self.HEIGHT//2) ]



    # takes input from human and give it to handle_events()
    def keyup(self, event):
        if event.key == K_UP:
            self.tickspeed +=30
        elif event.key == K_DOWN:
            self.tickspeed -=30
            if(self.tickspeed<=1):
                self.tickspeed=5


    # handles human input, useless (and unused) for ML argos
    def handle_events(self):
        for event in pygame.event.get():

            if event.type == KEYUP:
                self.keyup(event)

            if(event.type == pygame.MOUSEBUTTONDOWN):

                pos = pygame.mouse.get_pos()
                self.request_newpos(pos)

            elif event.type == QUIT:
                sys.exit() # quits program if you press x


    # no idea what is supposed to be returned,
    # but almost no algorithm uses the returnvalue anyway,
    # renders the stuff onto the pygame.Surface
    def render(self, mode='human', close=None):

        self.__draw()
        pygame.display.update()
        self.fps.tick()
        return "renderreturn"

    # make screenshot and return it as a numpy array
    def getSS(self):
        image = pygame.Surface((self.WIDTH, self.HEIGHT))  # Create image surface
        image.blit(self.screen, (0, 0), ((0,0), (self.WIDTH, self.HEIGHT)))  # Blit portion of the display to the image

        imgstring = pygame.image.tostring(image, "RGBA",False)
        # pygame.image.save(image, "screenshot.jpg")  # Save the image to the disk
        nparr = np.fromstring(imgstring,np.uint8)
        dimnparr = nparr.reshape((400,600,4)).astype("uint8")

        # from PIL import Image
        # ymage = Image.fromarray(dimnparr, "RGBA")
        # ymage.show()
        return dimnparr

    # this method can be used to play as a human, if True
    # if False the game plays itself only using random actions
    # a ML algo could be inserted here, but for OO reasons in an extra file
    # if not human, random actions
    def start(self, human=True):

        counter = 0

        env = self
        observation = env.reset()
        frame = 0

        done = False
        while not done:
            frame+=1
            env.render()
            # print(observation)
            if(not human):
                action = env.action_space.sample()
                observation, reward, done, info = env.step(action)
            else:
                observation, reward, done, info = env.step()
                time.sleep(0.02) # 50 fps, uncomment to have it at "normal" speed

            if done:
                env.reset()
                done = False
                counter+=1
                print(counter) # game counter
                # env.close() # plays only 1 round and closes if uncommented


Simulation().start(True) # uncomment to play the game as human, by starting this file