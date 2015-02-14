# An Wu @CMU 2011
# the player class
# player.py


import math
import os
import copy
import time
import pygame
from pygame.locals import *
from load import *

# assume the game board is (1800, 1200)

class Player(pygame.sprite.Sprite):
    def __init__(self, gameData):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image, self.rect = load_image('player.png', -1)
        self.rect.center = (512, 384)
        self.life = gameData['life']
        self.die = False
        self.protecting = True
        self.direction = [0, 0]
        self.speedDir = [0, 0]
        self.boardSpeed = 8
        self.rotated = self.image
        self.boardPos = [900, 600]  #start at the middle of the board
        self.protectTime = 0
        self.speedRatio = 0
        self.acceleration = gameData['acceleration']
        self.xSpeedRatio = 0
        self.ySpeedRatio = 0
        self.rotateAngle = 0

    def walk(self):
        dirLen = (self.speedDir[0]**2 + self.speedDir[1]**2)**0.5
        if 140 < self.boardPos[0]+self.speedDir[0]*self.boardSpeed < 1660:
            self.boardPos[0] += self.speedDir[0] * self.boardSpeed / dirLen * \
                                self.xSpeedRatio
            centerList = [512 + (self.boardPos[0] - 900) / 8,
                          384 + (self.boardPos[1] - 600) / 8]
            self.rect.center = (centerList[0], centerList[1])
        if 140 < self.boardPos[1]-self.speedDir[1]*self.boardSpeed < 1060:
            self.boardPos[1] += -self.speedDir[1] * self.boardSpeed / dirLen * \
                                self.ySpeedRatio
            centerList = [512 + (self.boardPos[0] - 900) / 8,
                          384 + (self.boardPos[1] - 600) / 8]
            self.rect.center = (centerList[0], centerList[1])
        if self.xSpeedRatio < 1 and self.direction[0] != 0:
            self.xSpeedRatio += self.acceleration
        elif self.xSpeedRatio > 0 and self.direction[0] == 0:
            self.xSpeedRatio -= self.acceleration
            if self.xSpeedRatio < 0.2:
                self.xSpeedRatio = 0
                self.speedDir[0] = 0
        if self.ySpeedRatio < 1 and self.direction[1] != 0:
            self.ySpeedRatio += self.acceleration
        elif self.ySpeedRatio > 0 and self.direction[1] == 0:
            self.ySpeedRatio -= self.acceleration
            if self.ySpeedRatio < 0.2:
                self.ySpeedRatio = 0
                self.speedDir[1] = 0

    def rotate(self):
        center = self.rect.center
        rotateAngle = math.atan2(self.speedDir[1] * self.ySpeedRatio,
                                 self.speedDir[0] * self.xSpeedRatio)
        rotateAngle = math.degrees(rotateAngle)
        self.rotateAngle = rotateAngle
        rotate = pygame.transform.rotate
        self.rotated = pygame.transform.rotate(self.image, rotateAngle)
        self.rect = self.rotated.get_rect(center=center)
        
    def protect(self):
        if time.time() - self.protectTime < 3 or\
           3.3 < time.time() - self.protectTime < 3.6 or\
           3.9 < time.time() - self.protectTime < 4.2 or\
           4.5 < time.time() - self.protectTime < 4.8:
            return 1
        elif time.time() - self.protectTime > 5:
            self.protecting = False
            return 0
        
            
    
        
