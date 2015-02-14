# An Wu @CMU 2011
# geometryWar.py

import math
import random
import os
import time
import sys
import copy
import pickle
import pygame
from pygame.locals import *
import blitGame
from player import *
from movingObject import *
from load import *
from dataStore import *
from getEnemy import *
from spark import *

def main(gameData):
    
#Initialize Everything
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1024, 768))

# Get the fonts
    nameFont = pygame.font.Font(os.path.join('data',
                                             'Creator_Campotype_smcp.ttf'), 80)
    numberFont = pygame.font.Font(os.path.join('data', 'imagine_font.ttf'), 40)
    infoFont = pygame.font.Font(os.path.join('data', 'imagine_font.ttf'), 50)
    myName = nameFont.render('Geometry Wars', False, (180, 180, 180))
    courseName = nameFont.render('15 112', False, (180, 180, 180))
    scoreFont = numberFont.render('SCORE', False, (200, 200, 200))
    pinFont = numberFont.render('PIN', False, (200, 200, 200))
    finalScore = numberFont.render('Final Score: ', False, (200, 200, 200))
    namePrompt = numberFont.render('Please Enter Your Name:', False,
                                   (200, 200, 200))
    pinBase = gameData['pinBase']
    price1 = numberFont.render(str(pinBase) + ' PIN', False,
                               (210, 210, 210))
    price2 = numberFont.render(str(pinBase*2) + ' PIN', False,
                               (210, 210, 210))
    price3 = numberFont.render(str(pinBase*4) + ' PIN', False,
                               (210, 210, 210))
    price4 = numberFont.render(str(pinBase*8) + ' PIN', False,
                               (210, 210, 210))
    price5 = numberFont.render(str(pinBase*4) + ' PIN', False,
                               (210, 210, 210))
    price6 = numberFont.render(str(pinBase*3) + ' PIN', False,
                               (210, 210, 210))
    storePrompt = numberFont.render('Click on Icon to Purchase', False,
                                    (220, 220, 220))
    waveHold = numberFont.render('Hold :', False, (200, 200, 200))
    

# Get audio object
    if gameData['name'] == 'wave':
        pygame.mixer.music.load(os.path.join('data', 'wave.ogg'))
    elif gameData['name'] == 'pacifism':
        pygame.mixer.music.load(os.path.join('data', 'pacifism.ogg'))
    else:
        pygame.mixer.music.load(os.path.join('data', 'maintheme.ogg'))
    shootBullet = pygame.mixer.Sound(os.path.join('data', 'bullet.wav'))
    boom = pygame.mixer.Sound(os.path.join('data', 'Boom.wav'))
    boomSmall = pygame.mixer.Sound(os.path.join('data', 'Boom_small.wav'))
    boomLarge = pygame.mixer.Sound(os.path.join('data', 'Boom_large.wav'))
    shieldDamage = pygame.mixer.Sound(os.path.join('data', 'shield_damage.wav'))
    shieldDown = pygame.mixer.Sound(os.path.join('data', 'shield_down.wav'))
    updateSound = pygame.mixer.Sound(os.path.join('data', 'update.ogg'))
    gameOverSound = pygame.mixer.Sound(os.path.join('data', 'gameover.ogg'))
    typeSound = pygame.mixer.Sound(os.path.join('data', 'type.wav'))
    
    
#Create the background
    try:
        background = pygame.image.load(pickle.load(open('save/back', 'rb')))
    except:
        background = pygame.image.load(setBackground)
    background = background.convert()
    playerIcon = pygame.image.load('data/playerIcon.png').convert()
    playerIcon.set_colorkey((0, 0, 0))
    bombIcon = pygame.image.load('data/bombIcon.png').convert()
    bombIcon.set_colorkey((0, 0, 0))
    pauseIcon = pygame.image.load('data/pause.png').convert()
    pauseIcon.set_colorkey((0, 0, 0))
    pauseInfo = pygame.font.Font('data/imagine_font.ttf', 80).render(\
                'GAME PAUSED', False, (200, 200, 200))
    updateIcon = pygame.image.load('data/updateIcon.png').convert()
    updateIcon.set_colorkey((0, 0, 0))
    protectIcon = pygame.image.load('data/protectIcon.png').convert()
    protectIcon.set_colorkey((0, 0, 0))
    greyBackground = pygame.image.load('data/greyBackground.png').convert()
    greyBackground.set_alpha(150)
    miniBack = pygame.image.load('data/miniBackground.png').convert()
    storeIcon = pygame.image.load('data/storeSample.png').convert()
    playerImg = pygame.image.load('data/player.png').convert()
    playerImg.set_colorkey((0, 0, 0))
    bulletImg = pygame.image.load('data/bullet.png').convert()
    bulletImg.set_colorkey((0, 0, 0))
    bulRot1 = pygame.transform.rotate(bulletImg, 5)
    bulRot2 = pygame.transform.rotate(bulletImg, -5)
    bulRot3 = pygame.transform.rotate(bulletImg, 10)
    bulRot4 = pygame.transform.rotate(bulletImg, -10)
    


#Prepare Game Objects
    player = Player(gameData)
    player.sparkTime = time.time()
    clock = pygame.time.Clock()
    gameTime = time.time()-3
    blinkInterval = 0.3
    r, g, b = 150, 150, 150
    rgbAdder = 2
    bulletInterval = 0.3
    protectNumber = 0
    pause = False
    exitGame = False
    manualExit = False
    bulletsRelease = False
    getMini = False
    spark = []
    end = False
    hold = False
    bulLev2 = False
    bulLev3 = False
    bulLev4 = False
    bulLev5 = False
    pygame.mixer.music.play(-1)

#Prepare Game data
    enemy1, enemy2, enemy3, enemy4, enemy5, enemy5D, enemy6, blink, bullets = \
    gameData['enemy1'], gameData['enemy2'], gameData['enemy3'], \
    gameData['enemy4'], gameData['enemy5'], gameData['enemy5D'], \
    gameData['enemy6'], gameData['blink'], gameData['bullets']
    gameScore = gameData['gameScore']
    gamePin = gameData['gamePin']
    bulletTime = gameData['bulletTime']
    bulletsLevel = gameData['bulletsLevel']
    bombNumber = gameData['bombNumber']
    level = gameData['level']
    enemyCounter = gameData['enemyCounter']
    
    

#Prepare game grids
    pointList1 = []
    xStart = 100
    yStart = 150
    adder = 1600
    sign = -1
    while xStart != 1700 or yStart != 1100:
        pointList1.append((xStart, yStart))
        if adder == 1600 or adder == -1600:
            xStart += adder
            adder = 50
        elif adder == 50:
            yStart += adder
            adder = 1600 * sign
            sign = -sign
    pointList2 = []
    xStart = 150
    yStart = 100
    adder = 1000
    sign = -1
    while xStart != 1700 or yStart != 1100:
        pointList2.append((xStart, yStart))
        if adder == 1000 or adder == -1000:
            yStart += adder
            adder = 50
        elif adder == 50:
            xStart += adder
            adder = 1000 * sign
            sign = -sign

            

# Main Loop
    while 1:
        clock.tick(50)
        if level == 1:
            if time.time() - gameTime > 0.8 * gameData['waveTime']:
                if gameData['name'] == 'wave':
                    player.protectTime = time.time() - 5
                    for enemy in gameData['enemyWave1']:
                        blink.append(MovingObject('enemy2',
                                     center=copy.deepcopy(enemy[0]),
                                     speed=8,
                                     direction=copy.deepcopy(enemy[1])))
                elif gameData['name'] == 'follower':
                    for i in xrange(4):
                        blink.append(MovingObject('enemy3',
                                        center=[200+1400*(i/2), 200+800*(i%2)],
                                        speed=4, direction=[1, 0]))                                              
                else:
                    getEnemy(player, level1Enemy, blink)
                    if gameData['name'] == 'pacifism':
                        blink.append(MovingObject('enemy6',center=None,speed=1))
                gameTime = time.time()
                enemyCounter += 1
            if enemyCounter == int(gameData['counterBase']*0.6):
                enemyCounter = 0
                level += 1
                
        elif level == 2:
            if time.time() - gameTime > gameData['waveTime']:
                if gameData['name'] == 'wave':
                    for enemy in gameData['enemyWave2']:
                        blink.append(MovingObject('enemy2',
                                     center=copy.deepcopy(enemy[0]),
                                     speed=8,
                                     direction=copy.deepcopy(enemy[1])))
                elif gameData['name'] == 'follower':
                    for i in xrange(4):
                        blink.append(MovingObject('enemy4',
                                        center=[200+1400*(i/2), 200+800*(i%2)],
                                        speed=3,
                                        direction = [1, 0]))
                else:
                    getEnemy(player, level2Enemy, blink)
                    if gameData['name'] == 'pacifism':
                        blink.append(MovingObject('enemy6',center=None,speed=1))
                gameTime = time.time()
                enemyCounter += 1
            if enemyCounter == int(gameData['counterBase']*0.8):
                enemyCounter = 0
                level += 1
        elif level == 3:
            if time.time() - gameTime > 0.9 * gameData['waveTime']:
                if gameData['name'] == 'wave':
                    for enemy in gameData['enemyWave3']:
                        blink.append(MovingObject('enemy2',
                                     center=copy.deepcopy(enemy[0]),
                                     speed=8,
                                     direction=copy.deepcopy(enemy[1])))
                elif gameData['name'] == 'follower':
                    if enemy3 == [] and enemy4 == []:
                        return True
                else:
                    getEnemy(player, level3Enemy, blink)
                    if gameData['name'] == 'pacifism':
                        blink.append(MovingObject('enemy6',center=None,speed=1))
                        blink.append(MovingObject('enemy6',center=None,speed=1))
                gameTime = time.time()
                enemyCounter += 1
            if enemyCounter == int(gameData['counterBase']):
                enemyCounter = 0
                level += 1
        elif level == 4:
            if time.time() - gameTime > 1.3 * gameData['waveTime']:
                if gameData['name'] == 'wave':
                    for enemy in gameData['enemyWave4']:
                        blink.append(MovingObject('enemy2',
                                     center=copy.deepcopy(enemy[0]),
                                     speed=8,
                                     direction=copy.deepcopy(enemy[1])))
                    hold = True
                    holdTime = time.time()
                else:
                    getEnemy(player, level4Enemy, blink)
                    if gameData['name'] == 'pacifism':
                        blink.append(MovingObject('enemy6',center=None,speed=1))
                        blink.append(MovingObject('enemy6',center=None,speed=1))
                gameTime = time.time()
                enemyCounter += 1
            if hold:
                gameTime = time.time()
            if enemyCounter == int(gameData['counterBase']*1.2):
                enemyCounter = 0
                level += 1
            if gameData['name'] == 'wave' and (not end) and hold:
                gaveTime = time.time()
        elif level == 5:
            if time.time() - gameTime > 1.2 * gameData['waveTime']:
                getEnemy(player, level5Enemy, blink)
                if gameData['name'] == 'pacifism':
                    blink.append(MovingObject('enemy6',center=None,speed=1))
                    blink.append(MovingObject('enemy6',center=None,speed=1))
                    blink.append(MovingObject('enemy6',center=None,speed=1))
                gameTime = time.time()
                enemyCounter += 1
            if enemyCounter == int(gameData['counterBase']*1.4):
                enemyCounter = 0
                level += 1
                decTime = 1.3 * gameData['waveTime']
        elif level == 6:
            if time.time() - gameTime > decTime:
                getEnemy(player, level5Enemy, blink)
                getEnemy(player, level2Enemy, blink)
                getEnemy(player, level1Enemy, blink)
                if gameData['name'] == 'pacifism':
                    blink.append(MovingObject('enemy6',center=None,speed=1))
                    blink.append(MovingObject('enemy6',center=None,speed=1))
                    blink.append(MovingObject('enemy6',center=None,speed=1))
                gameTime = time.time()
                enemyCounter += 1
            if enemyCounter == int(gameData['counterBase']*0.5):
                enemyCounter = 0
                decTime = decTime * 0.8

        r += rgbAdder
        g += rgbAdder
        b += rgbAdder
        if r > 250:
            rgbAdder = -2
        elif r < 100:
            rgbAdder = 2
        
    # Handle Input
        for event in pygame.event.get():
        # Pause
            if (event.type == MOUSEBUTTONDOWN and event.button == 1 and
                485 < event.pos[0] < 515 and 40 < event.pos[1] < 70) or\
               (event.type == KEYDOWN and event.key == K_f):
                pygame.mixer.music.pause()
                pause = True
                while 1:
                    for event in pygame.event.get():
                        if (event.type == MOUSEBUTTONDOWN and event.button == 1
                            and 485 < event.pos[0] < 515 and
                            40 < event.pos[1] < 70) or (event.type == KEYDOWN
                            and event.key == K_f):
                            pause = False
                    if pause == False:
                        pygame.mixer.music.unpause()
                        break
                # blit everything
                    blitGame.blit(player, enemy1, enemy2, enemy3,
                                  enemy4, enemy5, enemy5D, enemy6, spark,
                    bullets, background, pointList1, pointList2, blink,
                    blinkInterval, myName, r, g, b, gameScore,
                    gamePin, numberFont, scoreFont, pinFont, playerIcon,
                    pauseIcon, updateIcon, bombIcon, bombNumber,protectIcon,
                    protectNumber,courseName,getMini,miniBack,screen,False)
                    screen.blit(greyBackground, (0, 0))
                    screen.blit(pauseInfo, (210, 350))
                # pause Icon
                    screen.blit(pauseIcon, (480, 35))
                    pygame.display.flip()
                player.direction = [0, 0]

        # Buy weapon
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and
                  530 < event.pos[0] < 560 and 40 < event.pos[1] < 70) or\
                 (event.type == KEYDOWN and event.key == K_g):
                pygame.mixer.music.pause()
                storeExit = False
                while 1:
                # handle Events
                    for event in pygame.event.get():
                        if (event.type == MOUSEBUTTONDOWN and
                            event.button == 1 and 530 < event.pos[0] < 560 and
                            40 < event.pos[1] < 70) or\
                           (event.type == KEYDOWN and event.key == K_g):
                            storeExit = True
                        if event.type == MOUSEBUTTONDOWN and\
                           event.button == 1:
                            if 100 < event.pos[0] < 190 and\
                               200 < event.pos[1] < 290:
                                if gamePin >= pinBase and\
                                   gameData['name'] != 'pacifism' and\
                                   bulletsLevel<2:
                                    updateSound.play()
                                    gamePin -= pinBase
                                    bulletsLevel = 2
                                    bulLev2 = True
                            elif 100 < event.pos[0] < 190 and\
                                    330 < event.pos[1] < 420:
                                if gamePin >= pinBase*2 and\
                                   gameData['name'] != 'pacifism' and\
                                   bulletsLevel<3:
                                    updateSound.play()
                                    gamePin -= pinBase*2
                                    bulletsLevel = 3
                                    bulLev3 = True
                            elif 100 < event.pos[0] < 190 and\
                                    460 < event.pos[1] < 550:
                                if gamePin >= pinBase*4 and\
                                   gameData['name'] != 'pacifism' and\
                                   bulletsLevel<4:
                                    updateSound.play()
                                    gamePin -= pinBase*4
                                    bulletsLevel = 4
                                    bulLev4 = True
                            elif 560 < event.pos[0] < 650 and\
                                 gameData['name'] != 'pacifism' and\
                                 200 < event.pos[1] < 290:
                                if gamePin >= pinBase*8 and bulletsLevel<5:
                                    updateSound.play()
                                    gamePin -= pinBase*8
                                    bulletsLevel = 5
                                    bulLev5 = True
                            elif 560 < event.pos[0] < 650 and\
                                    330 < event.pos[1] < 420:
                                if gamePin >= pinBase*4 and \
                                    protectNumber==0 and\
                                    gameData['name'] != 'follower':
                                    updateSound.play()
                                    gamePin -= pinBase*4
                                    protectNumber+=1
                            elif 560 < event.pos[0] < 650 and\
                                 gameData['name'] != 'pacifism' and\
                                 460 < event.pos[1] < 550:
                                if gamePin >= pinBase*3 and\
                                    bombNumber < 3 and\
                                    gameData['name'] != 'follower':
                                    updateSound.play()
                                    gamePin -= pinBase*3
                                    bombNumber += 1
                                            
                                        
                    if storeExit:
                        pygame.mixer.music.unpause()
                        break
                # blit everything
                    blitGame.blit(player, enemy1, enemy2, enemy3,
                                    enemy4, enemy5, enemy5D, enemy6, spark,
                    bullets, background, pointList1, pointList2, blink,
                    blinkInterval, myName, r, g, b, gameScore,
                    gamePin, numberFont, scoreFont, pinFont, playerIcon,
                    pauseIcon, updateIcon, bombIcon, bombNumber,protectIcon,
                    protectNumber,courseName,getMini,miniBack,screen,False)
                    screen.blit(greyBackground, (0, 0))
                    for row in xrange(3):
                        for col in xrange(2):
                            screen.blit(storeIcon, (100+col*460,
                                                    200+row*130))
                            if not (row > 0 and col == 1):
                                screen.blit(playerImg, (107+col*460,
                                                        220+row*130))
                    screen.blit(bulRot1, (155, 230))
                    screen.blit(bulRot2, (155, 245))
                    screen.blit(bulletImg, (155, 368))
                    screen.blit(bulRot1, (154, 355))
                    screen.blit(bulRot2, (154, 380))
                    screen.blit(bulRot1, (155, 490))
                    screen.blit(bulRot2, (155, 505))
                    screen.blit(bulRot3, (153, 475))
                    screen.blit(bulRot4, (153, 520))
                    screen.blit(bulletImg, (615, 236))
                    screen.blit(bulRot1, (614, 223))
                    screen.blit(bulRot2, (614, 249))
                    screen.blit(bulRot3, (612, 210))
                    screen.blit(bulRot4, (612, 262))
                    screen.blit(playerImg, (583, 351))
                    pygame.draw.circle(screen, (240, 240, 240), (605, 375),
                                        32, 5)
                    pygame.draw.circle(screen, (240, 240, 240), (605, 505),
                                       30, 4)
                    pygame.draw.circle(screen, (240, 240, 240), (605, 505),
                                       10, 4)
                    screen.blit(price1, (300, 220))
                    screen.blit(price2, (300, 350))
                    screen.blit(price3, (300, 480))
                    screen.blit(price4, (760, 220))
                    screen.blit(price5, (760, 350))
                    screen.blit(price6, (760, 480))
                    screen.blit(storePrompt, (100, 650))
                    if bulLev2:
                        pygame.draw.rect(screen, (0, 220, 0),
                                         (100, 200, 90, 90), 3)
                    if bulLev3:
                        pygame.draw.rect(screen, (0, 220, 0),
                                         (100, 330, 90, 90), 3)
                    if bulLev4:
                        pygame.draw.rect(screen, (0, 220, 0),
                                         (100, 460, 90, 90), 3)
                    if bulLev5:
                        pygame.draw.rect(screen, (0, 220, 0),
                                         (560, 200, 90, 90), 3)
                    if gameData['name'] == 'follower':
                        pygame.draw.rect(screen, (220, 0, 0),
                                         (560, 330, 88, 88), 4)
                        pygame.draw.rect(screen, (220, 0, 0),
                                         (560, 460, 88, 88), 4)
                    elif gameData['name'] == 'pacifism':
                        pygame.draw.rect(screen, (220, 0, 0),
                                         (100, 200, 88, 88), 4)
                        pygame.draw.rect(screen, (220, 0, 0),
                                         (100, 330, 88, 88), 4)
                        pygame.draw.rect(screen, (220, 0, 0),
                                         (100, 460, 88, 88), 4)
                        pygame.draw.rect(screen, (220, 0, 0),
                                         (560, 200, 88, 88), 4)
                        pygame.draw.rect(screen, (220, 0, 0),
                                         (560, 460, 88, 88), 4)

                # update Icon
                    screen.blit(updateIcon, (524, 34))
                    pygame.display.flip()

                player.direction = [0, 0]
                        
           
            # Release Bullets        
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                bulletsRelease = True
                mpos = event.pos
                
            if event.type == MOUSEBUTTONUP and event.button == 1:
                bulletsRelease = False

            if bulletsRelease:
                if event.type == MOUSEMOTION:
                    mpos = event.pos    

        # use protection
            if event.type == MOUSEBUTTONDOWN and event.button == 3 and \
               protectNumber == 1:
                player.protecting = True
                protectNumber=0
                
        # Move player
            if event.type == KEYDOWN:
                if event.key == K_w: player.direction[1] += 1
                elif event.key == K_a: player.direction[0] -= 1
                elif event.key == K_d: player.direction[0] += 1
                elif event.key == K_s: player.direction[1] -= 1
                elif event.key == K_m: getMini = not getMini
                elif event.key == K_SPACE:  #Release Bomb
                    if bombNumber != 0:
                        boomLarge.play()
                        for enemy in enemy1+enemy2+enemy3+enemy4+enemy5+enemy5D:
                            spark.append(Spark(enemy.boardPos, 30, 30))
                        enemy1, enemy2, enemy3, enemy4, enemy5, enemy5D,enemy6,\
                        bullets = [], [], [], [], [], [], [], []
                        bombNumber -= 1
                        
            elif event.type == KEYUP:
                if event.key == pygame.K_w: player.direction[1] -= 1
                elif event.key == pygame.K_a: player.direction[0] += 1
                elif event.key == pygame.K_d: player.direction[0] -= 1
                elif event.key == pygame.K_s: player.direction[1] += 1
                elif event.key == K_ESCAPE:
                    exitGame = True
                    manualExit = True
                    if gameData['name'] == 'wave' or \
                       gameData['name'] == 'follower':
                        return False

        if player.direction[0] != 0:
            player.speedDir[0] = player.direction[0]
        if player.direction[1] != 0:
            player.speedDir[1] = player.direction[1]
        if player.speedDir != [0, 0]:
            player.rotate()
            player.walk()
            if time.time() - player.sparkTime > 0.07:
                rotateRadians = math.radians(player.rotateAngle)
                boardPos = [player.boardPos[0]-20*math.cos(rotateRadians),
                            player.boardPos[1]+20*math.sin(rotateRadians)]
                spark.append(Spark(boardPos, 15, 3, 2,
                                   player.rotateAngle-10, 20, True))
                player.sparkTime = time.time()
            

    # Move enemy
        for enemy in enemy1:
            if enemy.die == True:
                gameScore += 10
                gamePin += 1
                spark.append(Spark(enemy.boardPos, 25, 20))
                enemy1.remove(enemy)
                boom.play()
            else:
                enemy.walk(player.rect.center, player.boardPos)
        for enemy in enemy2:
            if enemy.die == True:
                gameScore += 30
                gamePin += 2
                spark.append(Spark(enemy.boardPos, 30, 25))
                enemy2.remove(enemy)
                boom.play()
            else:
                enemy.walk(player.rect.center, player.boardPos)
        for enemy in enemy3:
            if enemy.die == True:
                gameScore += 40
                gamePin += 2
                spark.append(Spark(enemy.boardPos, 30, 25))
                enemy3.remove(enemy)
                boom.play()
            else:
                enemy.follow(player.rect.center, player.boardPos)
        for enemy in enemy4:
            if enemy.die == True:
                gameScore += 80
                gamePin += 4
                spark.append(Spark(enemy.boardPos, 40, 35))
                enemy4.remove(enemy)
                boom.play()
            else:
                enemy.follow(player.rect.center, player.boardPos)
        for enemy in enemy5:
            if enemy.die == True:
                gameScore += 40
                gamePin += 2
                spark.append(Spark(enemy.boardPos, 30, 30))
                enemy5.remove(enemy)
                boom.play()
            else:
                enemy.walk(player.rect.center, player.boardPos)
                enemy.rotate(1)
        for enemy in enemy5D:
            if enemy.die == True:
                gameScore += 10
                gamePin += 1
                spark.append(Spark(enemy.boardPos, 20, 15))
                enemy5D.remove(enemy)
                boomSmall.play()
            else:
                enemy.walk(player.rect.center, player.boardPos)
                enemy.rotate(2)
        for enemy in enemy6:
            if enemy.die == True:
                gameScore += 20
                gamePin += 2
                spark.append(Spark(copy.copy(player.boardPos), 40, 35))
                enemy6.remove(enemy)
                boom.play()
            else:
                enemy.enemy6rotate(player.rect.center, player.boardPos)
                

    # Release Bullets        
        if bulletsRelease == True and gameData['allowBullets']:
            if time.time() - bulletTime > bulletInterval:
                bpos = copy.copy(player.boardPos)
                ppos = [player.rect.center[0], player.rect.center[1]]
                bdir = [mpos[0] - ppos[0], -mpos[1] + ppos[1]]
                bdirLen = (bdir[0]**2 + bdir[1]**2)**0.5
                factor = 40.0/bdirLen  #Zero devision error here?
                bdir = [bdir[0]*factor, bdir[1]*factor]
                bdirRad = math.atan2(bdir[1], bdir[0])
                bulletTime = time.time()
                shootBullet.play()
                if bulletsLevel == 1:
                    bullets.append(MovingObject('bullet', center=bpos, speed=1,
                                                direction=bdir))
                elif bulletsLevel == 2:
                    b2dir = [(40 * math.cos(bdirRad + 0.05)),
                             (40 * math.sin(bdirRad + 0.05))]
                    b3dir = [(40 * math.cos(bdirRad - 0.05)),
                             (40 * math.sin(bdirRad - 0.05))]
                    bullets.append(MovingObject('bullet',
                                                center=copy.copy(bpos), speed=1,
                                                direction=b2dir))
                    bullets.append(MovingObject('bullet',
                                                center=copy.copy(bpos), speed=1,
                                                direction=b3dir))
                elif bulletsLevel == 3:
                    b2dir = [(40 * math.cos(bdirRad + 0.08)),
                             (40 * math.sin(bdirRad + 0.08))]
                    b3dir = [(40 * math.cos(bdirRad - 0.08)),
                             (40 * math.sin(bdirRad - 0.08))]
                    bullets.append(MovingObject('bullet', center=bpos, speed=1,
                                                direction=copy.copy(bdir)))
                    bullets.append(MovingObject('bullet',
                                                center=copy.copy(bpos), speed=1,
                                                direction=b2dir))
                    bullets.append(MovingObject('bullet',
                                                center=copy.copy(bpos), speed=1,
                                                direction=b3dir))
                elif bulletsLevel == 4:
                    b2dir = [(40 * math.cos(bdirRad + 0.04)),
                             (40 * math.sin(bdirRad + 0.04))]
                    b3dir = [(40 * math.cos(bdirRad - 0.04)),
                             (40 * math.sin(bdirRad - 0.04))]
                    b4dir = [(40 * math.cos(bdirRad + 0.12)),
                             (40 * math.sin(bdirRad + 0.12))]
                    b5dir = [(40 * math.cos(bdirRad - 0.12)),
                             (40 * math.sin(bdirRad - 0.12))]
                    bullets.append(MovingObject('bullet', center=bpos, speed=1,
                                                direction=b2dir))
                    bullets.append(MovingObject('bullet',
                                                center=copy.copy(bpos), speed=1,
                                                direction=b3dir))
                    bullets.append(MovingObject('bullet',
                                                center=copy.copy(bpos), speed=1,
                                                direction=b4dir))
                    bullets.append(MovingObject('bullet',
                                                center=copy.copy(bpos), speed=1,
                                                direction=b5dir))
                elif bulletsLevel == 5:
                    b2dir = [(40 * math.cos(bdirRad + 0.08)),
                             (40 * math.sin(bdirRad + 0.08))]
                    b3dir = [(40 * math.cos(bdirRad - 0.08)),
                             (40 * math.sin(bdirRad - 0.08))]
                    b4dir = [(40 * math.cos(bdirRad + 0.16)),
                             (40 * math.sin(bdirRad + 0.16))]
                    b5dir = [(40 * math.cos(bdirRad - 0.16)),
                             (40 * math.sin(bdirRad - 0.16))]
                    bullets.append(MovingObject('bullet',
                                                center=copy.copy(bpos), speed=1,
                                                direction=copy.copy(bdir)))
                    bullets.append(MovingObject('bullet',
                                                center=copy.copy(bpos), speed=1,
                                                direction=b2dir))
                    bullets.append(MovingObject('bullet',
                                                center=copy.copy(bpos), speed=1,
                                                direction=b3dir))
                    bullets.append(MovingObject('bullet',
                                                center=copy.copy(bpos), speed=1,
                                                direction=b4dir))
                    bullets.append(MovingObject('bullet',
                                                center=copy.copy(bpos), speed=1,
                                                direction=b5dir))
                
                    
        for bullet in bullets:
            if bullet.die == True:
                bullets.remove(bullet)
            else:
                bullet.walk(player.rect.center, player.boardPos)

    # Check collision
        for enemy in enemy1+enemy2+enemy3+enemy5D:
            for bullet in bullets:
                if pygame.sprite.collide_rect_ratio(0.8)(bullet, enemy):
                    bullets.remove(bullet)
                    enemy.die = True
        for enemy in enemy4:
            for bullet in bullets:
                if pygame.sprite.collide_rect_ratio(0.8)(bullet, enemy):
                    bullets.remove(bullet)
                    enemy.life -= 1
                    spark.append(Spark(enemy.boardPos, 15, 20))
                    shieldDamage.play()
                    if enemy.life == 0:
                        enemy.die = True
        for enemy in enemy5:
            for bullet in bullets:
                if pygame.sprite.collide_rect_ratio(0.8)(bullet, enemy):
                    bullets.remove(bullet)
                    enemy.die = True
                    for drow in [-1, 1]:
                        for dcol in [-1, 1]:
                            enemy5D.append(MovingObject('enemy5D',
                                           center=copy.copy(enemy.boardPos),
                                           speed=10,
                                           direction=[drow, dcol]))
        for enemy in enemy1+enemy2+enemy3+enemy4+enemy5+enemy5D:
            if pygame.sprite.collide_rect_ratio(0.55)(player, enemy):
                if time.time() - player.protectTime < 5:
                    enemy.die = True
                else:
                    player.die = True
                    collideEnemy = enemy
        for enemy in enemy6:
            enemySlope = -math.tan(math.radians(enemy.rotateStart))
            if ((player.rect.center[0] - enemy.realCenter[0])**2 +
                (player.rect.center[1] - enemy.realCenter[1])**2) < 9900:
                reference = player.rect.center[0]*enemySlope +\
                            enemy.realCenter[1] - enemy.realCenter[0]*enemySlope
                distance = 10*(enemySlope**2 + 1)**0.5
                if player.rect.center[1]-distance < reference < \
                   player.rect.center[1]+distance:
                    enemy.die = True
                    for inChar in enemy1+enemy2+enemy3+enemy4+enemy5+enemy5D:
                        if inChar.name != 'enemy6':
                            if ((inChar.rect.center[0]-player.rect.center[0])**2
                           +(inChar.rect.center[1]-player.rect.center[1])**2)< \
                            62500:
                                inChar.die = True
        for sparkObj in spark:
            if sparkObj.die:
                spark.remove(sparkObj)
            
                    
    # Check player life
        if player.die == True:
            if player.life > 0:
                player.life -= 1
                enemyCounter -= 2
                blinkTime = time.time()
                pygame.mixer.music.stop()
                gameOverSound.play()
            # blink collided enemy
                while 1:
                    backgroundPlace = (-288 + (900-player.boardPos[0])/10,
                                      -216 + (600-player.boardPos[1])/10)
                    screen.blit(background, backgroundPlace)
                    # Draw background grids
                    realList1, realList2 = [], []
                    for point in pointList1:
                        realList1.append((point[0]+player.rect.center[0]-\
                                          player.boardPos[0],
                            point[1]+player.rect.center[1]-player.boardPos[1]))
                    for point in pointList2:
                        realList2.append((point[0]+player.rect.center[0]-\
                                          player.boardPos[0],
                            point[1]+player.rect.center[1]-player.boardPos[1]))
                    pygame.draw.lines(screen, (0, 0, 100), False, realList1)
                    pygame.draw.lines(screen, (0, 0, 100), False, realList2)
                    pygame.draw.rect(screen, (r, g, b),
                         (player.rect.center[0] - player.boardPos[0] + 100,
                          player.rect.center[1] - player.boardPos[1] + 100,
                          1600, 1000), 10)
                # Get myname panel
                    myNameCenter = (430 + (900 - player.boardPos[0])/10.0,
                                    (200 - player.boardPos[1])/5.0)
                    screen.blit(myName, myNameCenter)
                # Draw outmost frame
                    pygame.draw.rect(screen, (r, g, b),
                         (player.rect.center[0] - player.boardPos[0],
                          player.rect.center[1] - player.boardPos[1],
                          1800, 1200), 10)
                    if time.time() - blinkTime < 0.4 or \
                       0.8 < time.time() - blinkTime < 1.2 or \
                       1.6 < time.time() - blinkTime < 2.0 or \
                       2.4 < time.time() - blinkTime < 2.8:
                        screen.blit(player.rotated, player.rect)
                        screen.blit(collideEnemy.rotated, collideEnemy.rect)
                    elif time.time() - blinkTime > 3.6:
                        break
                    for i in xrange(player.life):
                        screen.blit(playerIcon, (400 + 25*i, 40))
                    for i in xrange(bombNumber):
                        screen.blit(bombIcon, (574 + 25*i, 40))
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
                    scoreNumber = numberFont.render(str(gameScore),
                                                    False, (200, 200, 200))
                    pinNumber = numberFont.render(str(gamePin),
                                                  False, (200, 200, 200))
                    screen.blit(scoreNumber, (60, 70))
                    screen.blit(pinNumber, (880, 70))
                 
                # pause Icon
                    screen.blit(pauseIcon, (480, 35))
    
                # update Icon
                    screen.blit(updateIcon, (524, 34))
                    pygame.display.flip()
                enemy1, enemy2, enemy3, enemy4, enemy5, enemy5D, enemy6,\
                blink, bullets = \
                [], [], [], [], [], [], [], [], []
                player.boardPos = [900, 600]
                player.rect.center = (512, 384)
                player.xSpeedRatio = 0
                player.ySpeedRatio = 0
                player.protecting = True
                player.die = False
                spark = []
                pygame.mixer.music.play()
        if player.life == 0:
            if gameData['name'] == 'wave' or gameData['name'] == 'follower':
                return
            elif gameData['name'] == 'pacifism':
                return gameScore
            exitGame = True
                
    
        
    # exit the game
        if exitGame:
            pygame.mixer.music.stop()
            if manualExit:
                if gameData['name'] == 'wave' or gameData['name'] == 'follower':
                    return
                elif gameData['name'] == 'pacifism':
                    return gameScore
                return ('ANONYMOUS', gameScore)
            else:
                score = numberFont.render(str(gameScore), False,(200, 200, 200))
                scoreWidth = score.get_width()
                playerName = ''
                while 1:
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_BACKSPACE:
                                playerName = playerName[:-1]
                            elif event.key == K_SPACE:
                                playerName = playerName + ' '
                            elif event.key == K_RETURN:
                                if playerName == '':
                                    playerName = 'ANONYMOUS'
                                return (playerName, gameScore)
                            elif ('a' <= pygame.key.name(event.key) <= 'z' or \
                                 '0' <= pygame.key.name(event.key) <= '9') and\
                                 len(pygame.key.name(event.key)) == 1:
                                typeSound.play()
                                playerName += pygame.key.name(event.key)
                    nameIcon = numberFont.render(playerName, False,
                                                 (200, 200, 200))
                    nameWidth = nameIcon.get_width()
                    blitGame.blit(player, enemy1, enemy2, enemy3,
                                    enemy4, enemy5, enemy5D, enemy6, spark,
                        bullets, background, pointList1, pointList2, blink,
                        blinkInterval, myName, r, g, b, gameScore,
                        gamePin, numberFont, scoreFont, pinFont, playerIcon,
                        pauseIcon, updateIcon, bombIcon, bombNumber,protectIcon,
                        protectNumber,courseName,getMini,miniBack,screen,False)
                    screen.blit(greyBackground, (0, 0))
                    screen.blit(finalScore, (370, 150))
                    screen.blit(score, (530 - scoreWidth/2, 250))
                    screen.blit(namePrompt, (250, 400))
                    screen.blit(nameIcon, (530-nameWidth/2, 500))
                    pygame.display.flip()
                return gameScore
                
    # blit everything
        blitGame.blit(player, enemy1, enemy2, enemy3, enemy4, enemy5, enemy5D,
                      enemy6,
                      spark, bullets, background, pointList1, pointList2, blink,
                      blinkInterval, myName, r, g, b, gameScore,
                      gamePin, numberFont, scoreFont, pinFont, playerIcon,
                      pauseIcon, updateIcon, bombIcon, bombNumber, protectIcon,
                      protectNumber, courseName, getMini, miniBack, screen)





                
