# An Wu @CMU 2011
# playGame.py


import pygame
import os
import time
import sys
import copy
import pickle
from pygame.locals import *
import geometryWars
from dataStore import *

def fade(screen, image, white, grey, clock, fadeOut=True):
    time1 = time.time()
    alphaValue = 0
    fadeExit = False
    if fadeOut:
        while time.time() - time1 < 6:
            clock.tick(70)
            image.set_alpha(alphaValue)
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    fadeExit = True
            if 1.5 > time.time() - time1:
                screen.blit(white, (0, 0))
                if alphaValue < 255:
                    alphaValue += 5
            elif time.time() - time1 > 4.5:
                screen.blit(grey, (0, 0))
                if alphaValue > 0:
                    alphaValue -= 3
            if fadeExit:
                break
            screen.blit(image, (0, 0))
            pygame.display.flip()
    else:
        while time.time() - time1 < 0.4:
            clock.tick(70)
            image.set_alpha(alphaValue)
            if 1 > time.time() - time1:
                screen.blit(white, (0, 0))
                if alphaValue < 255:
                    alphaValue += 10
            screen.blit(image, (-1, 0))
            pygame.display.flip()
    


def main():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    time1 = time.time()
    screen = pygame.display.set_mode((1024, 768))
    screen.fill((255, 255, 255))


#Create the background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((30,30,30))
    r, g, b = 220, 220, 220
    rgbAdder = 5
    nextIcon = pygame.image.load('data/nextIcon.png').convert()
    nextIcon.set_colorkey((0, 0, 0))
    pythonIcon = pygame.image.load('data/pythonIcon.png').convert()
    white = pygame.image.load('data/whiteBackground.png').convert()
    grey = pygame.image.load('data/greyBackground.png').convert()
    regularBack = pygame.image.load('data/RegularBack.png').convert()
    gameIntro = pygame.image.load('data/instruction.png').convert()
    official = pygame.image.load('data/official.jpg').convert()
    black = pygame.image.load('data/blackBackground.png').convert()

#Get audio files
    pygame.mixer.music.load(os.path.join('data', 'main.ogg'))


#Prepare game grids
    pointList1 = []
    xStart = 0
    yStart = 0
    adder = 1100
    sign = -1
    while xStart != 1100 or yStart != 800:
        pointList1.append((xStart, yStart))
        if adder == 1100 or adder == -1100:
            xStart += adder
            adder = 50
        elif adder == 50:
            yStart += adder
            adder = 1100 * sign
            sign = -sign
    pointList2 = []
    xStart = 30
    yStart = 0
    adder = 800
    sign = -1
    while xStart != 1130 or yStart != 0:
        pointList2.append((xStart, yStart))
        if adder == 800 or adder == -800:
            yStart += adder
            adder = 50
        elif adder == 50:
            xStart += adder
            adder = 800 * sign
            sign = -sign

# get the first 6 High Scores
    def getHighScores(scores):
        scores = copy.deepcopy(scores)
        max6 = []
        n = 6
        if len(scores) < 6:
            n = len(scores)
        for i in xrange(n):
            maxScore = 0
            name = ''
            for pair in scores:
                if pair[1] >= maxScore:
                    maxScore = pair[1]
                    name = pair[0]
            max6.append((name, maxScore))
            scores.remove((name, maxScore))
        return max6
            

# Get Text
    font1 = pygame.font.Font('data/transFont.ttf', 120)
    menu = pygame.font.Font('data/NEUROPOL.ttf', 60)
    numberFont = pygame.font.Font('data/imagine_font.ttf', 50)
    title = font1.render('Geometry Wars', False, (200, 200, 200))
    titleCenter = (512, 100)
    startGame = menu.render('Start Game', False, (180, 180, 180))
    highScore = menu.render('High Score', False, (180, 180, 180))
    challenges = menu.render('Challenges', False, (180, 180, 180))
    settings = menu.render('Settings', False, (180, 180, 180))
    highScoreIcon = font1.render('High Scores', False, (200, 200, 200))
    settingsIcon = font1.render('Settings', False, (200, 200, 200))
    numberFontB = pygame.font.Font('data/imagine_font.ttf', 70)
    numberFontC = pygame.font.Font('data/imagine_font.ttf', 30)
    introIcon = menu.render('Game Intro', False, (200, 200, 200))
    difficultyIcon = menu.render('Difficulty', False, (200, 200, 200))
    difTitle = font1.render('Difficulty', False, (200, 200, 200))
    easyIcon = menu.render('Easy', False, (200, 200, 200))
    normalIcon = menu.render('Normal', False, (200, 200, 200))
    difficultIcon = menu.render('Difficult', False, (200, 200, 200))
    backgroundIcon = menu.render('Background', False, (200, 200, 200))
    backgroundCenter = (512, 384)
    backFont = pygame.font.Font('data/English_.ttf', 60)
    gameIntroFont = numberFont.render('In-Game Instructions', False,
                                      (200, 200, 200))
    chalTitle = font1.render('Challenges', False, (200, 200, 200))
    waveIcon = menu.render('Wave', False, (200, 200, 200))
    followerIcon = menu.render('Follower', False, (200, 200, 200))
    pacifismIcon = menu.render('Pacifism', False, (200, 200, 200))

# Initialize Data
    try:
        gameScores = pickle.load(open('save/highScores', 'rb'))
    except:
        gameScores = []

# fade in start
    pygame.mixer.music.play(-1)
    fade(screen, pythonIcon, white, black, clock)
    fade(screen, official, black, grey, clock)
    fade(screen, regularBack, grey, grey, clock, False)
    
    

# Main loop
    while 1:
        clock.tick(40)
        for event in pygame.event.get():       
            if event.type == MOUSEBUTTONUP and event.button == 1:
            # start game
                try:
                    difficultyLevel = pickle.load(open('save/difficulty', 'rb'))
                except:
                    pickle.dump('easy', (open('save/difficulty', 'wb')))
                    difficultyLevel = 'easy'
                if difficultyLevel == 'easy':
                    gameData = copy.deepcopy(easyGame)
                elif difficultyLevel == 'normal':
                    gameData = copy.deepcopy(normalGame)
                elif difficultyLevel == 'difficult':
                    gameData = copy.deepcopy(hardGame)                   
                if 60 < event.pos[0] < 460 and 280 < event.pos[1] < 380:
                    pygame.mixer.music.stop()
                    game = geometryWars.main(copy.deepcopy(gameData))
                    pygame.mixer.music.load(os.path.join('data', 'main.ogg'))
                    pygame.mixer.music.play(-1)
                    gameScores.append((game[0], game[1]))
                    pickle.dump(gameScores, open('save/highScores','wb'))

            # set game
                elif 550 < event.pos[0] < 950 and 380 < event.pos[1] < 480:
                    setExit = False
                    while 1:
                        clock.tick(40)
                    # handle events
                        for event in pygame.event.get():
                            if event.type == KEYUP and\
                               event.key == K_ESCAPE:
                                setExit = True
                            if event.type==MOUSEBUTTONUP and event.button == 1:
                            # intro to game
                                if 280 < event.pos[0] < 730 and\
                                   300 < event.pos[1] < 400:
                                    introExit = False
                                    while 1:
                                        clock.tick(40)
                                    # handle events
                                        for event in pygame.event.get():
                                            if event.type == KEYUP and\
                                               event.key == K_ESCAPE:
                                                introExit = True
                                        if introExit:
                                            break
                                        screen.blit(gameIntro, (0, 0))
                                        screen.blit(gameIntroFont, (30, 40))
                                        pygame.display.flip()


                                                
                            # change difficulty level
                                if event.type == MOUSEBUTTONUP and\
                                   40 < event.pos[0] < 490 and\
                                   500 < event.pos[1] < 600:
                                    difExit = False
                                    while 1:
                                        clock.tick(40)
                                    # handle events
                                        for event in pygame.event.get():
                                            if event.type == KEYUP and\
                                               event.key == K_ESCAPE:
                                                difExit = True
                                            elif event.type==MOUSEBUTTONDOWN:
                                                if 290 < event.pos[0] < 740 and\
                                                   270 < event.pos[1] < 370:
                                                    difficulty = 'easy'
                                                    pickle.dump(difficulty,
                                                                open('save/'+
                                                    'difficulty', 'wb'))
                                                elif 290 <event.pos[0]< 740 and\
                                                   420 < event.pos[1] < 520:
                                                    difficulty = 'normal'
                                                    pickle.dump(difficulty,
                                                                open('save/'+
                                                    'difficulty', 'wb'))
                                                elif 290 <event.pos[0]< 740 and\
                                                   570 < event.pos[1] < 670:
                                                    difficulty = 'difficult'
                                                    pickle.dump(difficulty,
                                                                open('save/'+
                                                    'difficulty', 'wb'))
                                        screen.blit(background, (0, 0))
                                        pygame.draw.lines(screen, (0, 0, 100),
                                                          False, pointList1)
                                        pygame.draw.lines(screen, (0, 0, 100),
                                                          False, pointList2)
                                        if difExit:
                                            break
                                        screen.blit(difTitle,
                                        difTitle.get_rect(center=titleCenter))
                                    # prepare straight line RGB
                                        if r > 220:
                                            rgbAdder = -5
                                        elif r < 100:
                                            rgbAdder = 5
                                        r += rgbAdder
                                        g += rgbAdder
                                        b += rgbAdder
                                        pygame.draw.line(screen, (r, g, b),
                                                         (0, 200), (1024, 200),
                                                         10)
                                        pygame.draw.line(screen, (r, g, b),
                                                         (0, 170), (1024, 170),
                                                         10)
                                        pygame.draw.line(screen, (r, g, b),
                                                         (0, 740), (1024, 740),
                                                         10)
                                        screen.blit(easyIcon, (420, 290))
                                        pygame.draw.rect(screen, (r, g, b),
                                                         (290, 270, 450, 100),
                                                         2)
                                        screen.blit(normalIcon, (400, 440))
                                        pygame.draw.rect(screen, (r, g, b),
                                                         (290, 420, 450, 100),
                                                         2)
                                        screen.blit(difficultIcon, (400, 590))
                                        pygame.draw.rect(screen, (r, g, b),
                                                         (290, 570, 450, 100),
                                                         2)
                                        difLv =\
                                    pickle.load(open('save/difficulty', 'rb'))
                                        if difLv == 'easy':
                                            pygame.draw.rect(screen, (0,250,0),
                                                         (290, 270, 450, 100),
                                                         2)
                                        elif difLv == 'normal':
                                            pygame.draw.rect(screen, (0,250,0),
                                                         (290, 420, 450, 100),
                                                         2)
                                        else:
                                            pygame.draw.rect(screen, (0,250,0),
                                                         (290, 570, 450, 100),
                                                         2)
                                        pygame.display.flip()

                                        
                            # change game background
                                if event.type == MOUSEBUTTONUP and\
                                    540 < event.pos[0] < 990 and\
                                   500 < event.pos[1] < 600:
                                    backExit = False
                                    changeBack = 'data/1.jpg'
                                    changeTitle = backFont.render('Wood', False,
                                                                  (200,200,200))
                                    changePrompt = backFont.render(
                                        'Enter to Confirm', False,(200,200,200))
                                    while 1:
                                    # handle events
                                        for event in pygame.event.get():
                                            if event.type == KEYUP:
                                                if event.key == K_ESCAPE:
                                                    backExit = True
                                                elif event.key == K_RETURN:
                                                    setBackground = changeBack
                                                    backExit = True
                                                    pickle.dump(setBackground,
                                                    open('save/back', 'wb'))
                                            if event.type==MOUSEBUTTONDOWN and\
                                               820 < event.pos[0] < 970 and\
                                               350 < event.pos[1] < 430:
                                                if changeBack == 'data/1.jpg':
                                                    changeBack = 'data/2.jpg'
                                                    changeTitle = backFont.\
                                                        render('Canvas', False,
                                                        (200,200,200))
                                                elif changeBack == 'data/2.jpg':
                                                    changeBack = 'data/3.jpg'
                                                    changeTitle = backFont.\
                                                        render('Galaxy', False,
                                                        (200,200,200))
                                                elif changeBack == 'data/3.jpg':
                                                    changeBack = 'data/1.jpg'
                                                    changeTitle = backFont.\
                                                        render('Wood', False,
                                                        (200,200,200))
                                        back = pygame.image.load(changeBack)
                                        screen.blit(back, back.get_rect(
                                                    center=backgroundCenter))
                                        screen.blit(changeTitle, (40, 30))
                                        screen.blit(changePrompt, (40, 650))
                                        screen.blit(nextIcon, (820, 350))
                                        pygame.display.flip()
                                        if backExit:
                                            break
                                            

                        if setExit:
                            break
                        screen.blit(background, (0, 0))
                        pygame.draw.lines(screen, (0, 0, 100),
                                          False, pointList1)
                        pygame.draw.lines(screen, (0, 0, 100),
                                          False, pointList2)
                        screen.blit(settingsIcon,
                                    settingsIcon.get_rect(center=titleCenter))
                        screen.blit(introIcon, (340, 320))
                        screen.blit(difficultyIcon, (110, 520))
                        screen.blit(backgroundIcon, (560, 520))
                        # prepare straight line RGB
                        if r > 220:
                            rgbAdder = -5
                        elif r < 100:
                            rgbAdder = 5
                        r += rgbAdder
                        g += rgbAdder
                        b += rgbAdder
                        pygame.draw.line(screen, (r, g, b),
                                         (0, 200), (1024, 200), 10)
                        pygame.draw.line(screen, (r, g, b),
                                         (0, 170), (1024, 170), 10)
                        pygame.draw.line(screen, (r, g, b),
                                         (0, 740), (1024, 740), 10)
                        pygame.draw.rect(screen, (r, g, b),
                                         (280, 300, 450, 100), 2)
                        pygame.draw.rect(screen, (r, g, b),
                                         (40, 500, 450, 100), 2)
                        pygame.draw.rect(screen, (r, g, b),
                                         (540, 500, 450, 100), 2)
                        pygame.display.flip()


            # Game Challenges    
                elif 60 < event.pos[0] < 460 and 480 < event.pos[1] < 580:
                    challengeExit = False
                    while 1:
                        clock.tick(40)
                    # handle events
                        for event in pygame.event.get():
                            if event.type == KEYUP and event.key == K_ESCAPE:
                                challengeExit = True
                            elif event.type == MOUSEBUTTONDOWN:
                                if 290 < event.pos[0] < 740 and\
                                   240 < event.pos[1] < 360:
                                    time1 = time.time()
                                    geometryWars.main(copy.deepcopy(waveGame))
                                    time2 = time.time()
                                    pygame.mixer.music.load(os.path.join('data',
                                                                    'main.ogg'))
                                    pygame.mixer.music.play(-1)
                                    try:
                                        cha1Time = pickle.load(open('save/cha1',
                                                                    'rb'))
                                    except:
                                        cha1Time = 0
                                    if round(time2-time1, 2) > cha1Time:
                                        pickle.dump(round(time2-time1, 2),
                                                    open('save/cha1', 'wb'))
                                if 290 < event.pos[0] < 740 and\
                                   400 < event.pos[1] < 520:
                                    time1 = time.time()
                                    geometryWars.main(copy.deepcopy(
                                        followerGame))
                                    time2 = time.time()
                                    pygame.mixer.music.load(os.path.join('data',
                                                                    'main.ogg'))
                                    pygame.mixer.music.play(-1)
                                    try:
                                        cha1Time = pickle.load(open('save/cha2',
                                                                    'rb'))
                                    except:
                                        cha2Time = 0
                                    if round(time2-time1, 2) > cha2Time:
                                        pickle.dump(round(time2-time1, 2),
                                                    open('save/cha2', 'wb'))
                                if 290 < event.pos[0] < 740 and\
                                   560 < event.pos[1] < 680:
                                    game = geometryWars.main(
                                        copy.deepcopy(pacifismGame))
                                    pygame.mixer.music.load(os.path.join('data',
                                                                    'main.ogg'))
                                    pygame.mixer.music.play(-1)
                                    try:
                                        cha3Score = pickle.load(open('save/cha3',
                                                                    'rb'))
                                    except:
                                        cha3Score = 0
                                    if game > cha3Score:
                                        pickle.dump(game,
                                                    open('save/cha3', 'wb'))
                        if challengeExit:
                            break
                        # prepare straight line RGB
                        if r > 220:
                            rgbAdder = -5
                        elif r < 100:
                            rgbAdder = 5
                        r += rgbAdder
                        g += rgbAdder
                        b += rgbAdder
                        screen.blit(background, (0, 0))
                        pygame.draw.lines(screen, (0, 0, 100),
                                          False, pointList1)
                        pygame.draw.lines(screen, (0, 0, 100),
                                          False, pointList2)
                        screen.blit(waveIcon, (420, 250))
                        pygame.draw.rect(screen, (r, g, b),(290, 240, 450, 120),
                                         2)
                        screen.blit(followerIcon, (390, 410))
                        pygame.draw.rect(screen, (r, g, b),(290, 400, 450, 120),
                                         2)
                        screen.blit(pacifismIcon, (380, 570))
                        pygame.draw.rect(screen, (r, g, b),(290, 560, 450, 120),
                                         2)
                        pygame.draw.line(screen, (r, g, b),
                                         (0, 200), (1024, 200), 10)
                        pygame.draw.line(screen, (r, g, b),
                                         (0, 170), (1024, 170), 10)
                        pygame.draw.line(screen, (r, g, b),
                                         (0, 740), (1024, 740), 10)
                        try:
                            cha1Time = pickle.load(open('save/cha1', 'rb'))
                            cha1TimeIcon = numberFontC.render(str(cha1Time) +
                                                ' s', False, (200, 200, 200))
                        except:
                            cha1TimeIcon = numberFontC.render('0.00 s', False,
                                                             (200, 200, 200))
                        screen.blit(cha1TimeIcon, cha1TimeIcon.get_rect(
                                    center=(518, 340)))
                        try:
                            cha2Time = pickle.load(open('save/cha2', 'rb'))
                            cha2TimeIcon = numberFontC.render(str(cha2Time) +
                                                ' s', False, (200, 200, 200))
                        except:
                            cha2TimeIcon = numberFontC.render('0.00 s', False,
                                                             (200, 200, 200))
                        screen.blit(cha2TimeIcon, cha2TimeIcon.get_rect(
                                    center=(518, 500)))
                        try:
                            cha3Score = pickle.load(open('save/cha3', 'rb'))
                            cha3ScoreIcon = numberFontC.render(str(cha3Score) +
                                                ' pts', False, (200, 200, 200))
                                    
                        except:
                            cha3ScoreIcon = numberFontC.render('0 pts', False,
                                                              (200, 200, 200))
                        screen.blit(cha3ScoreIcon, cha3ScoreIcon.get_rect(
                                    center=(518, 660)))
                        screen.blit(chalTitle,
                                    chalTitle.get_rect(center=titleCenter))
                        pygame.display.flip()
                        

            # Get High Scores
                elif 550 < event.pos[0] < 950 and 580 < event.pos[1] < 680:
                    highScoreExit = False
                # render high scores
                    highScoresRender = []
                    counter = 1
                    for pair in getHighScores(gameScores):
                        highScoresRender.append(numberFont.render(
                            str(counter)+'. '+pair[0], False, (200, 200, 200)))
                        highScoresRender.append(numberFont.render(
                            str(pair[1]), False, (200, 200, 200)))
                        counter += 1
                    while 1:
                        clock.tick(40)
                        for event in pygame.event.get():
                            if event.type == KEYUP and\
                               event.key == K_ESCAPE:
                                highScoreExit = True
                        if highScoreExit:
                            break
                        screen.blit(background, (0, 0))
                        pygame.draw.lines(screen, (0, 0, 100),
                                          False, pointList1)
                        pygame.draw.lines(screen, (0, 0, 100),
                                          False, pointList2)
                        screen.blit(highScoreIcon,
                                    highScoreIcon.get_rect(center=titleCenter))
                    # draw high scores
                        counter = 0
                        for item in highScoresRender:
                            if counter%2 == 0:
                                screen.blit(item, (100, 250+80*(counter/2)))
                            else:
                                screen.blit(item, (900 - item.get_width(),
                                                   250 + 80*(counter/2)))
                            counter += 1
                    # prepare straight line RGB
                        if r > 220:
                            rgbAdder = -5
                        elif r < 100:
                            rgbAdder = 5
                        r += rgbAdder
                        g += rgbAdder
                        b += rgbAdder
                        pygame.draw.line(screen, (r, g, b),
                                         (0, 200), (1024, 200), 10)
                        pygame.draw.line(screen, (r, g, b),
                                         (0, 170), (1024, 170), 10)
                        pygame.draw.line(screen, (r, g, b),
                                         (0, 740), (1024, 740), 10)
                        pygame.display.flip()
                        
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mixer.music.stop()
                    sys.exit()

                
        screen.blit(background, (0, 0))
        pygame.draw.lines(screen, (0, 0, 100), False, pointList1)
        pygame.draw.lines(screen, (0, 0, 100), False, pointList2)
        screen.blit(title, title.get_rect(center=titleCenter))

    # prepare straight line RGB
        if r > 215:
            rgbAdder = -5
        elif r < 100:
            rgbAdder = 5
        r += rgbAdder
        g += rgbAdder
        b += rgbAdder
        pygame.draw.line(screen, (r, g, b),
                         (0, 200), (1024, 200), 10)
        pygame.draw.line(screen, (r, g, b),
                         (0, 170), (1024, 170), 10)
    # Draw Menu items
        screen.blit(startGame, (80, 300))
        pygame.draw.rect(screen, (r, g, b),
                         (60, 280, 400, 100), 2)
        screen.blit(settings, (620, 400))
        pygame.draw.rect(screen, (r, g, b),
                         (550, 380, 400, 100), 2)
        screen.blit(challenges, (85, 500))
        pygame.draw.rect(screen, (r, g, b),
                         (60, 480, 400, 100), 2)
        screen.blit(highScore, (580, 600))
        pygame.draw.rect(screen, (r, g, b),
                         (550, 580, 400, 100), 2)
        pygame.display.flip()

main()
