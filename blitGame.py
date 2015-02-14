# An Wu @CMU 2011
# blitGame.py
# blit everything on the background

import math, os, time
import pygame
from pygame.locals import *

def blit(player, enemy1, enemy2, enemy3, enemy4, enemy5, enemy5D, enemy6, spark,
         bullets, background, pointList1, pointList2, blink, blinkInterval,
         myName, r, g, b, gameScore, gamePin, numberFont, scoreFont, pinFont,
         playerIcon, pauseIcon, updateIcon, bombIcon, bombNumber, protectIcon,
         protectNumber, courseName, getMini, miniBack, screen, flip=True):
# Blit background
    backgroundPlace = (-288 + (900-player.boardPos[0])/10,
                        -216 + (600-player.boardPos[1])/10)
    screen.blit(background, backgroundPlace)

        
# Draw background grids
    realList1, realList2 = [], []
    for point in pointList1:
        realList1.append((point[0]+player.rect.center[0]-player.boardPos[0],
                        point[1]+player.rect.center[1]-player.boardPos[1]))
    for point in pointList2:
        realList2.append((point[0]+player.rect.center[0]-player.boardPos[0],
                            point[1]+player.rect.center[1]-player.boardPos[1]))
    pygame.draw.lines(screen, (0, 0, 100), False, realList1)
    pygame.draw.lines(screen, (0, 0, 100), False, realList2)

# Blink enemies
    if flip:
        for enemy in blink:
            if time.time() - enemy.time < blinkInterval or \
                2*blinkInterval < time.time() - enemy.time < 3*blinkInterval or\
                4*blinkInterval < time.time() - enemy.time < 5*blinkInterval:
                enemy.blink(player.rect.center, player.boardPos, screen)
            elif 5*blinkInterval < time.time() - enemy.time:
                if enemy.name=='enemy1':
                    enemy1.append(enemy)
                elif enemy.name=='enemy2':
                    enemy2.append(enemy)
                elif enemy.name=='enemy3':
                    enemy3.append(enemy)
                elif enemy.name=='enemy4':
                    enemy4.append(enemy)
                elif enemy.name=='enemy5':
                    enemy5.append(enemy)
                elif enemy.name=='enemy6':
                    enemy6.append(enemy)
                blink.remove(enemy)
    else:
        for enemy in blink:
            enemy.time = time.time()
    screen.blit(player.rotated, player.rect)

# player protection
    if flip:
        if player.protecting:
            player.protectTime = time.time()
            player.protecting = False
        if player.protect():
            pygame.draw.circle(screen, (255, 255, 255),
                               player.rect.center, 29, 5)
    else:
        player.protectTime = time.time() - 4
        
# blit enemy+bullets
    for character in enemy1+enemy2+enemy3+enemy4+enemy5+enemy5D+enemy6+bullets:
        screen.blit(character.rotated, character.rect)
                        

    
# Get myname panel
    myNameCenter = (320 + (900 - player.boardPos[0])/10.0,
                    (200 - player.boardPos[1])/4.0)
    screen.blit(myName, myNameCenter)

# Get course name panel
    courseNameCenter = (430 + (900 - player.boardPos[0])/10.0,
                              (3000 - player.boardPos[1])/3.0)
    screen.blit(courseName, courseNameCenter)
    
# Draw outmost Frame
    pygame.draw.rect(screen, (r, g, b),
                     (player.rect.center[0] - player.boardPos[0] + 100,
                      player.rect.center[1] - player.boardPos[1] + 100,
                      1600, 1000), 10)
    pygame.draw.rect(screen, (r, g, b),
                     (player.rect.center[0] - player.boardPos[0],
                      player.rect.center[1] - player.boardPos[1],
                      1800, 1200), 10)

# blit spark
    if flip:
        for sparkObj in spark:
            sparkObj.drawSpark(screen, player.rect.center, player.boardPos)

# minimap
    if getMini:
        screen.blit(miniBack, (796, 600))
        for enemy in enemy1+enemy2+enemy3+enemy4+enemy5+enemy5D:
            pygame.draw.circle(screen, (220, 0, 0),
                               (787 + int(enemy.boardPos[0]/8),
                                600 + int(enemy.boardPos[1]/8)),
                               2)
        pygame.draw.circle(screen, (200, 200, 200),
                           (787 + int(player.boardPos[0]/8),
                            600 + int(player.boardPos[1]/8)),
                            3) 

# score and pin panel
    screen.blit(scoreFont, (60, 40))
    screen.blit(pinFont, (880, 40))
    scoreNumber = numberFont.render(str(gameScore), False, (200, 200, 200))
    pinNumber = numberFont.render(str(gamePin), False, (200, 200, 200))
    screen.blit(scoreNumber, (60, 70))
    screen.blit(pinNumber, (880, 70))

# life panel
    for i in xrange(player.life):
        screen.blit(playerIcon, (380 + 25*i, 40))
# bomb panel
    for i in xrange(bombNumber):
        screen.blit(bombIcon, (594 + 25*i, 40))

# pause Icon
    screen.blit(pauseIcon, (480, 35))
    
# update Icon
    screen.blit(updateIcon, (524, 34))

# protect Icon
    if protectNumber:
        screen.blit(protectIcon, (510, 75))

    
    if flip:
        pygame.display.flip()
