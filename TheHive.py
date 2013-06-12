#!/usr/bin/python
'''The Main Game Script

Does initialization and game looping'''

has_pygame = True

import TheHive
import sys
try:
    import pygame
    from pygame.locals import *
except ImportError:
    has_pygame = False

if has_pygame:
    #Initialize
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('The Hive v0.01')

W = TheHive.World()

print TheHive.HiveMath.getHexToXY(0,2,8)
print TheHive.HiveMath.normalHex(0,2,8)
print -2, -3, -1
print TheHive.HiveMath.getHexToXY(-2,-3,-1)
print TheHive.HiveMath.normalHex(-2,-3,-1)

#sys.exit(0)

#Loop
gameQuit = not has_pygame
while not gameQuit: # main game loop
    DISPLAYSURF.fill((0,0,0))
    W.update()
    W.draw(DISPLAYSURF)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            gameQuit = True
    W.clock.tick(12)
    #print W.bees 
    #Fs = [_H for _H in W.hexmap if W.hexmap[_H].terrain == 'Flower']
    #print len(Fs)

#Finish
#print W
print len(W.hexmap)
print len(W.normalhexmap)
print len(W.visiblehexmap)

for B in W.bees:
    print B.hexmap.keys()