#!/usr/bin/python
'''The Main Game Script

Does initialization and game looping'''

has_pygame = False

import TheHive
import sys
if has_pygame:
    import pygame
    from pygame.locals import *

    #Initialize
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('The Hive v0.01')

W = TheHive.World()

#Loop
gameQuit = not has_pygame
while not gameQuit: # main game loop
    DISPLAYSURF.fill((0,0,0))
    W.draw(DISPLAYSURF)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            gameQuit = True

#Finish
print W
print W.hexmap[(0,0,0)]
print W.hexmap[(-1,-1,1)]
print W.hexmap[(1,1,-1)]