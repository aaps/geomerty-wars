# An Wu @CMU 2011
# getEnemy.py
# add enemy to game

import random, time
from movingObject import *

def getEnemy(player, enemyList, blink):
    for enemy in enemyList:
    # Get enemy1
        if enemy == 'enemy1':
            playerPos = player.boardPos
            enemy1Choice = [[player.boardPos[0]+300, player.boardPos[1]+300],
                            [player.boardPos[0]+300, player.boardPos[1]-300],
                            [player.boardPos[0]-300, player.boardPos[1]+300],
                            [player.boardPos[0]-300, player.boardPos[1]-300]]                             
            blink.append(MovingObject('enemy1',
                                      center=random.choice(enemy1Choice),
                                      speed=1,
                                      direction=random.choice([[1, 1],[1, -1],
                                                        [-1, 1], [-1, -1]])))
    # Get enemy2
        elif enemy == 'enemy2':
            enemy2Choice1 = [[player.boardPos[0], 200],
                             [player.boardPos[0], 1000]]
            enemy2Choice2 = [[200, player.boardPos[1]],
                             [1600, player.boardPos[1]]]
            blink.append(MovingObject('enemy2',
                                      center=random.choice(enemy2Choice1),
                                      speed=9,
                                      direction=[0, 1]))
            blink.append(MovingObject('enemy2',
                                      center=random.choice(enemy2Choice2),
                                      speed=9,
                                      direction=[1, 0]))
    # Get enemy3
        elif enemy == 'enemy3':
            blink.append(MovingObject('enemy3', center=None, speed=4))
    # Get enemy4
        elif enemy == 'enemy4':
            blink.append(MovingObject('enemy4', center=None, speed=3))
    # Get enemy5
        elif enemy == 'enemy5':
            blink.append(MovingObject('enemy5', center=None, speed=6,
                                      direction=random.choice([[1, 1],[1, -1],
                                                        [-1, 1], [-1, -1]])))

    # Get enemy6
        elif enemy == 'enemy6':
            blink.append(MovingObject('enemy6', center=None, speed=1))
