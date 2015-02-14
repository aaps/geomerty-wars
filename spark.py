# An Wu @CMU 2011
# spark.py

import pygame
import math
import copy
import time
import random
from pygame.locals import *

class Spark(pygame.sprite.Sprite):
    def __init__(self, boardPos, radius, pieces, width=3, start=0,
                 revolution=360, color=None):
        self.boardPos = boardPos
        self.radius = radius
        self.time = time.time()
        self.die = False
        self.sparkList = []
        self.width = width
        if color==None:
            self.color = random.choice([(255, 255, 255), (255, 150, 150),
                                        (150, 255, 150), (150, 150, 255)])
        else:
            self.color = (220, 220, 220)
        self.speedRatio = 1
        for i in xrange(pieces):
            rad = math.radians(start+(revolution/pieces)*i)
            soloRadius = random.randint(int(0.5*radius), int(2*radius))
            self.sparkList.append([rad, copy.copy(self.boardPos),
                                [self.boardPos[0] -soloRadius*math.cos(rad)*3,
                                 self.boardPos[1] +soloRadius*math.sin(rad)*3],
                                soloRadius, self.speedRatio])

    def drawSpark(self, screen, playerCenter, playerBoardCenter):
        self.color = (self.color[0]-5, self.color[1]-5, self.color[2]-5)
        if self.color[0] < 0 or self.color[1] < 0 or self.color[2] < 0:
            self.color = (0, 0, 0)
        lengthMax = 0
        for spark in self.sparkList:
            startPos = (playerCenter[0] + spark[1][0] - playerBoardCenter[0],
                        playerCenter[1] + spark[1][1] - playerBoardCenter[1])
            endPos = (playerCenter[0] + spark[2][0] - playerBoardCenter[0],
                      playerCenter[1] + spark[2][1] - playerBoardCenter[1])
            pygame.draw.line(screen, self.color, startPos, endPos, self.width)
            spark[1][0] -= spark[3]*math.cos(spark[0])*0.7*spark[4]
            spark[1][1] += spark[3]*math.sin(spark[0])*0.7*spark[4]
            spark[2][0] -= spark[3]*math.cos(spark[0])*0.3*spark[4]
            spark[2][1] += spark[3]*math.sin(spark[0])*0.3*spark[4]
            if spark[4] > 0.2:
                spark[4] = spark[4]*0.8
            if (spark[1][0] - spark[2][0])**2 + \
               (spark[1][1] - spark[2][1])**2 > lengthMax:
                lengthMax = (spark[1][0] - spark[2][0])**2 +\
                            (spark[1][1] - spark[2][1])**2
        if lengthMax < 1:
            self.die = True




