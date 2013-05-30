#!/usr/bin/python
'''The Main Game Script

Does initialization and game looping'''

import TheHive
import sys
import pygame
from pygame.locals import *

#Initialize
pygame.init()
DISPLAYSURF = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('The Hive v0.01')

W = TheHive.World()

#Loop
gameQuit = False
while not gameQuit: # main game loop
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            gameQuit = True

#Finish
print W