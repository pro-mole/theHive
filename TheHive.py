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

#sys.exit(0)

#Loop
gameQuit = not has_pygame
fps = 12
tick = 0
while not gameQuit: # main game loop
    DISPLAYSURF.fill((0,0,0))
    if tick == 0:
        W.update()
    W.draw(DISPLAYSURF)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            gameQuit = True
    W.clock.tick(fps)
    tick = (tick + 1) % fps 
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