# An Wu @CMU 2011
# dataStore.py
# Store any saved data, and pre-data

import copy
from player import *
from movingObject import *

# game initials
easyGame = {}
normalGame = {}
hardGame = {}
waveGame = {}
followerGame = {}
pacifismGame = {}
setBackground = 'data/1.jpg'


# game elements
level1Enemy = ['enemy1', 'enemy1', 'enemy1', 'enemy1', 'enemy2']
level2Enemy = ['enemy1', 'enemy1', 'enemy1', 'enemy1',
               'enemy2', 'enemy2', 'enemy3', 'enemy3', 'enemy6']
level3Enemy = ['enemy1', 'enemy1', 'enemy1', 'enemy1',
               'enemy2', 'enemy2', 'enemy3', 'enemy3',
               'enemy3', 'enemy3', 'enemy4', 'enemy4', 'enemy6']
level4Enemy = ['enemy1', 'enemy1', 'enemy1', 'enemy1',
               'enemy2', 'enemy2', 'enemy3', 'enemy3',
               'enemy3', 'enemy4', 'enemy4', 'enemy5', 'enemy6']
level5Enemy = ['enemy1', 'enemy1', 'enemy2', 'enemy2',
               'enemy3', 'enemy3', 'enemy3', 'enemy3', 
               'enemy4', 'enemy4', 'enemy4', 'enemy4',
               'enemy5', 'enemy5', 'enemy5', 'enemy6']


# initialGame data
easyGame['name'] = 'easy'
easyGame['enemy1'] = []
easyGame['enemy2'] = []
easyGame['enemy3'] = []
easyGame['enemy4'] = []
easyGame['enemy5'] = []
easyGame['enemy5D'] = []
easyGame['enemy6'] = []
easyGame['bullets'] = []
easyGame['blink'] = []
easyGame['gamePin'] = 0
easyGame['life'] = 3
easyGame['bulletTime'] = 0
easyGame['bulletsLevel'] = 1
easyGame['gameScore'] = 0
easyGame['bombNumber'] = 3
easyGame['level'] = 1
easyGame['enemyCounter'] = 0
easyGame['waveTime'] = 7
easyGame['acceleration'] = 1/9.0
easyGame['pinBase'] = 25
easyGame['allowBullets'] = True
easyGame['counterBase'] = 8

normalGame['name'] = 'normal'
normalGame['enemy1'] = []
normalGame['enemy2'] = []
normalGame['enemy3'] = []
normalGame['enemy4'] = []
normalGame['enemy5'] = []
normalGame['enemy5D'] = []
normalGame['enemy6'] = []
normalGame['bullets'] = []
normalGame['blink'] = []
normalGame['gamePin'] = 0
normalGame['life'] = 3
normalGame['bulletTime'] = 0
normalGame['bulletsLevel'] = 1
normalGame['gameScore'] = 0
normalGame['bombNumber'] = 2
normalGame['level'] = 1
normalGame['enemyCounter'] = 1
normalGame['waveTime'] = 6
normalGame['acceleration'] = 1/8.0
normalGame['pinBase'] = 30
normalGame['allowBullets'] = True
normalGame['counterBase'] = 7

hardGame['name'] = 'hard'
hardGame['enemy1'] = []
hardGame['enemy2'] = []
hardGame['enemy3'] = []
hardGame['enemy4'] = []
hardGame['enemy5'] = []
hardGame['enemy5D'] = []
hardGame['enemy6'] = []
hardGame['bullets'] = []
hardGame['blink'] = []
hardGame['gamePin'] = 0
hardGame['life'] = 3
hardGame['bulletTime'] = 0
hardGame['bulletsLevel'] = 1
hardGame['gameScore'] = 0
hardGame['bombNumber'] = 1
hardGame['level'] = 2
hardGame['enemyCounter'] = 0
hardGame['waveTime'] = 5
hardGame['acceleration'] = 1/6.0
hardGame['pinBase'] = 35
hardGame['allowBullets'] = True
hardGame['counterBase'] = 6

waveGame['name'] = 'wave'
waveGame['enemy1'] = []
waveGame['enemy2'] = []
waveGame['enemy3'] = []
waveGame['enemy4'] = []
waveGame['enemy5'] = []
waveGame['enemy5D'] = []
waveGame['enemy6'] = []
waveGame['bullets'] = []
waveGame['blink'] = []
waveGame['life'] = 1
waveGame['gamePin'] = 0
waveGame['bulletTime'] = 0
waveGame['bulletsLevel'] = 1
waveGame['gameScore'] = 0
waveGame['bombNumber'] = 0
waveGame['level'] = 1
waveGame['enemyCounter'] = 0
waveGame['waveTime'] = 5
waveGame['acceleration'] = 1/6.0
waveGame['pinBase'] = 40
waveGame['allowBullets'] = False
waveGame['counterBase'] = 1.9
waveGame['enemyWave1'] = [([155 + 50*i, 160], [0, -1]) for i in xrange(16)]
waveGame['enemyWave2'] = [([895 + 50*i, 1045], [0, 1]) for i in xrange(16)]
waveGame['enemyWave3'] = [([160, 155 + 50*i], [1, 0]) for i in xrange(10)]
waveGame['enemyWave4'] = [([160, 595 + 50*i], [-1, 0]) for i in xrange(10)]

followerGame['name'] = 'follower'
followerGame['enemy1'] = []
followerGame['enemy2'] = []
followerGame['enemy3'] = []
followerGame['enemy4'] = []
followerGame['enemy5'] = []
followerGame['enemy5D'] = []
followerGame['enemy6'] = []
followerGame['bullets'] = []
followerGame['blink'] = []
followerGame['life'] = 1
followerGame['gamePin'] = 0
followerGame['bulletTime'] = 0
followerGame['bulletsLevel'] = 1
followerGame['gameScore'] = 0
followerGame['bombNumber'] = 0
followerGame['level'] = 1
followerGame['enemyCounter'] = 0
followerGame['waveTime'] = 1.0
followerGame['acceleration'] = 1/6.0
followerGame['pinBase'] = 25
followerGame['allowBullets'] = True
followerGame['counterBase'] = 30

pacifismGame['name'] = 'pacifism'
pacifismGame['enemy1'] = []
pacifismGame['enemy2'] = []
pacifismGame['enemy3'] = []
pacifismGame['enemy4'] = []
pacifismGame['enemy5'] = []
pacifismGame['enemy5D'] = []
pacifismGame['enemy6'] = []
pacifismGame['bullets'] = []
pacifismGame['blink'] = []
pacifismGame['life'] = 1
pacifismGame['gamePin'] = 0
pacifismGame['bulletTime'] = 0
pacifismGame['bulletsLevel'] = 1
pacifismGame['gameScore'] = 0
pacifismGame['bombNumber'] = 0
pacifismGame['level'] = 1
pacifismGame['enemyCounter'] = 0
pacifismGame['waveTime'] = 6
pacifismGame['acceleration'] = 1/6.0
pacifismGame['pinBase'] = 10
pacifismGame['allowBullets'] = False
pacifismGame['counterBase'] = 5
pacifismGame['enemyNumber'] = 3

