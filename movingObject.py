# An Wu @CMU 2011
# movingObject.py

import random, time, math
import pygame
from pygame.locals import *
from load import *

class MovingObject(pygame.sprite.Sprite):
    def __init__(self, name, center, speed, direction=None):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image, self.rect = load_image(name + '.png', -1)
        self.die = False
        self.boardSpeed = speed
        self.time = time.time()
        self.rotated = self.image
        self.rotatingCounter = 0
        if direction != None:
            self.direction = direction
        if (center != None and 150<center[0]<1650 and 150<center[1]<1050) or \
           self.name == 'bullet':
            self.boardPos = center
            angle = math.degrees(math.atan2(direction[1], direction[0]))
            self.rotated = pygame.transform.rotate(self.image, angle)
        elif self.name == 'enemy6':
            self.boardPos = [random.randint(250, 1400),
                             random.randint(200, 800)]
            self.rotateStart = 0
            self.rotating = random.choice([1, -1])
            self.realCenter = (0, 0)
            self.counter = 0
            
        else:
            self.boardPos = random.choice([[200, 200], [200, 1000],
                                           [1600, 200], [1600, 1000]])
        if self.name == 'enemy4':
            self.life = 3
    
    def walk(self, playerCenter, playerBoardCenter):
        self.rect.center = (playerCenter[0] + self.boardPos[0] -
                            playerBoardCenter[0],
                            playerCenter[1] + self.boardPos[1] -
                            playerBoardCenter[1])
        if self.boardPos[0] < 130 or self.boardPos[0] > 1670:
            self.direction[0] = -self.direction[0]
            if self.name == 'bullet':
                self.die = True
        if self.boardPos[1] < 130 or self.boardPos[1] > 1060:
            self.direction[1] = -self.direction[1]
            if self.name == 'bullet':
                self.die = True
        self.boardPos[0] += self.direction[0] * self.boardSpeed
        self.boardPos[1] += -self.direction[1] * self.boardSpeed
        if self.name == 'enemy2':
            if self.direction == [1, 0]:
                self.rotated = pygame.transform.rotate(self.image, -90)
            elif self.direction == [-1, 0]:
                self.rotated = pygame.transform.rotate(self.image, 90)
            elif self.direction == [0, 1]:
                self.rotated = self.image
            elif self.direction == [0, -1]:
                self.rotated = pygame.transform.rotate(self.image, 180)
            

    def follow(self, playerCenter, playerBoardCenter):
        self.rect.center = (playerCenter[0] + self.boardPos[0] -
                            playerBoardCenter[0],
                            playerCenter[1] + self.boardPos[1] -
                            playerBoardCenter[1])
        fdir = [playerBoardCenter[0] - self.boardPos[0],
                playerBoardCenter[1] - self.boardPos[1]]
        fdirLen = (fdir[0]**2 + fdir[1]**2)**0.5
        if fdirLen != 0:
            fdir = [fdir[0]/fdirLen, fdir[1]/fdirLen]
        self.fdir = fdir
        self.boardPos[0] += int(self.fdir[0] * self.boardSpeed)
        self.boardPos[1] += int(self.fdir[1] * self.boardSpeed)
        if self.name == 'enemy4':
            followRad = math.atan2(-fdir[1], fdir[0])
            self.rotated = pygame.transform.rotate(self.image,
                                                   math.degrees(followRad))

    def blink(self, playerCenter, playerBoardCenter, screen):
        self.rect.center = (playerCenter[0] + self.boardPos[0] -
                            playerBoardCenter[0],
                            playerCenter[1] + self.boardPos[1] -
                            playerBoardCenter[1])
        if self.name == 'enemy2':
            if self.direction == [1, 0]:
                self.rotated = pygame.transform.rotate(self.image, -90)
            elif self.direction == [-1, 0]:
                self.rotated = pygame.transform.rotate(self.image, 90)
            elif self.direction == [0, 1]:
                self.rotated = self.image
            elif self.direction == [0, -1]:
                self.rotated = pygame.transform.rotate(self.image, 180)
        screen.blit(self.rotated, self.rect)
        
    def rotate(self, angle):
        revolution = self.rotatingCounter
        self.rotated = pygame.transform.rotate(self.image, revolution*angle)
        self.rotatingCounter += 1

    def enemy6rotate(self, playerCenter, playerBoardCenter):
        self.counter += 1
        if self.counter == 2:
            self.rotateStart += self.rotating
            self.rotated = pygame.transform.rotate(self.image, self.rotateStart)
            self.rect.center = (playerCenter[0] + self.boardPos[0] -
                                playerBoardCenter[0],
                                playerCenter[1] + self.boardPos[1] -
                                playerBoardCenter[1])
            self.realCenter = (-110+self.rotated.get_rect().center[0]+
                               self.rect.center[0],
                               -15+self.rotated.get_rect().center[1]+
                               self.rect.center[1])
            self.counter = 0
        
    

