'''World module
codified how the world that this game happens in works'''

from BEE import BEE
from HiveMath import *
import hiveRand
import random
import math
import pygame
from pygame.locals import *

class Hex:
    '''Terrain type(e.g. Hive, Dirt, Leaf, Flower, Water, Sand)'''
    terrain = ''
    
    '''Smells
    Creatures in the world may leave smells where they pass, or around them; BEEs especially use them to mark paths and warnings; smells are characterized by flavor and intensity'''
    smells = None
    
    '''Containers'''
    '''Liquids(e.g. Honey, Water, Nectar)'''
    liquids = None
    '''Solids(e.g. Wax, Eggs, Dirt)'''
    solids = None
    '''Powders(e.g. Pollen, Sand, Salt, Sugar, Dust)'''
    powders = None
    
    def __init__(self, terrain):
        self.terrain = terrain
        self.smells = {}
        self.liquids = {}
        self.solids = {}
        self.powders = {}
    
    def __repr__(self):
        R = "{0} Hex({1})".format(self.terrain, id(self))
        R += "\n\tSmells like {0}".format(self.smells)
        R += "\n\tContains:"
        for container in (self.liquids, self.solids, self.powders):
            if len(container) > 0:
                R += "\n\t\t{0}".format(container)
        return R
     
    '''Adds smell to this Hex
    Smells cannot be smaller than 0'''
    def changeSmell(self, smell, intensity):
        if self.smells.has_key(smell):
            self.smells[smell] += intensity
        else:
            self.smells[smell] = intensity
        
        if self.smells[smell] < 0:
                self.smells.pop(smell)
    
    '''Adds liquid to this Hex
    Liquids cannot be smaller than 0'''
    def changeLiquid(self, liq, volume):
        if self.liquids.has_key(liq):
            self.liquids[liq] += volume
        else:
            self.liquids[liq] = volume
        
        if self.liquids[liq] < 0:
                self.liquids.pop(liq)
    
    '''Adds solids to this Hex
    Solids cannot be smaller than 0'''
    def changeSolid(self, solid, quantity):
        if self.solids.has_key(solid):
            self.solids[solid] += quantity
        else:
            self.solids[solid] = quantity
        
        if self.solids[solid] < 0:
                self.solids.pop(solid)
    
    '''Adds powder to this Hex
    Powders cannot be smaller than 0'''
    def changePowder(self, powder, weight):
        if self.powders.has_key(powder):
            self.powders[powder] += weight
        else:
            self.powders[powder] = weight
        
        if self.powders[powder] < 0:
                self.powders.pop(powder)
        
class World:

    '''Random seed. Really, REALLY important'''
    SEED = 0;
    
    '''Hex size; for drawing'''
    hexSize = 32;
    
    '''The Hex Map is a map of hex data list(smells, liquids, solids, terrain) to (H,I,J) positions'''
    hexmap = {}
    '''The Rect Map is a map of hex data list(smells, liquids, solids, terrain) to (X,Y) positions'''
    rectmap = {} 
    
    '''BEEs. We'll keep them all together for easy of use'''
    bees = []
    
    '''All entities'''
    entities = []
    
    '''Hive hexes'''
    hiveHex = []
    
    '''The Clock'''
    clock = None
    
    '''Create world loading all data necessary'''
    def __init__(self,**data):
        #No data; start over
        if len(data) == 0:
            for (i,j,k) in ((0,0,1),(0,1,0),(1,0,0),(-1,0,0),(0,-1,0),(0,0,-1),(0,0,0)):
                        H = self.addHex(i, j, k, type="Hive")
                        self.hiveHex.append(H)
            initrange = 1
            for h in range(-initrange,initrange+1):
                for i in range(-initrange,initrange+1):
                    for j in range(-initrange,initrange+1):
                        self.addHex(h,i,j)
            
            B = BEE(0,0,0,self)
            B.setFunction("QUEEN")
            self.bees.append(B)
            self.entities.append(B)
            for i in range(3):
                _p = [0,0,0]
                _p[i] = 1
                B = BEE(_p[0], _p[1], _p[2], self)
                self.bees.append(B)
                self.entities.append(B)
        
        hiveRand.seed = self.SEED
        self.clock = pygame.time.Clock()
            
    def __repr__(self):
        R = ""
        R += "TheHive World Object\n"
        R += "Loaded hexes: {0}\n".format(len(self.hexmap))
        for H in self.hexmap:
            R += "\t{0}\t{1}\n".format(H,self.hexmap[H])
        R += "\nBEEs: \n"
        for B in self.bees:
            R += "\t{0};\n".format(B)
        R += "\nEntities: \n"
        for E in self.entities:
            R += "\t{0};\n".format(E)
        
        return R
    
    '''Get hex in position H,I,J'''
    def getHex(self,h,i,j):
        if self.hexmap.has_key(normalHex(h,i,j)):
            return self.hexmap[normalHex(h,i,j)]
        else:
            return(self.addHex(h,i,j))
    
    '''Add new hex in position H,I,J(taking in account randomizations)'''
    def addHex(self,h,i,j,**hexdata):
        if not self.hexmap.has_key((h,i,j)):
            _h,_i,_j = normalHex(h,i,j)
            if not self.hexmap.has_key((_h,_i,_j)):
                random.seed(hiveRand.getSeedForHex((_h,_i,_j)))
                if hexdata.has_key('type'):
                    self.hexmap[(_h,_i,_j)] = Hex(hexdata['type'])
                else:
                    chance = random.random()
                    #Flowers on a 1% chance
                    if chance < 0.1:
                        self.hexmap[(_h,_i,_j)] = Hex('Flower')
                        self.hexmap[(_h,_i,_j)].changeLiquid('Honey',int(random.random() * 20))
                        self.hexmap[(_h,_i,_j)].changePowder('Pollen',int(random.random() * 50))
                        self.hexmap[(_h,_i,_j)].changeSmell('Flower',1)
#                         for d in range(1,5):
#                             self.getHex(_h+d,_i,_j).changeSmell('Flower', math.pow(2,-d))
#                             self.getHex(_h-d,_i,_j).changeSmell('Flower', math.pow(2,-d))
#                             self.getHex(_h,_i+d,_j).changeSmell('Flower', math.pow(2,-d))
#                             self.getHex(_h,_i-d,_j).changeSmell('Flower', math.pow(2,-d))
#                             self.getHex(_h,_i,_j+d).changeSmell('Flower', math.pow(2,-d))
#                             self.getHex(_h,_i,_j-d).changeSmell('Flower', math.pow(2,-d))
                    #Everything else is just plain ol' dirt   
                    else:
                        self.hexmap[(_h,_i,_j)] = Hex('Dirt')
            else:
                print "Collided adding Hex {0} [{1}]".format((h,i,j),(_h,_i,_j))
            self.hexmap[(h,i,j)] = self.hexmap[(_h,_i,_j)]
        _h,_i,_j = normalHex(h,i,j)
        return self.hexmap[(h,i,j)]
    
    def draw(self, surface):
        for H in self.hexmap:
            h,i,j = H
            x,y = getHexToXY(h, i, j)
            hexdata = self.getHex(h, i, j)
            C = None
            if hexdata.terrain == "Hive":
                C = pygame.Color(255,192,0)
            elif hexdata.terrain == "Dirt":
                C = pygame.Color(128,96,64)
            elif hexdata.terrain == "Flower":
                C = pygame.Color(255,192,220)
            
            #The hexagon "radius"
            h = self.hexSize / 2.0
            hexV = [(x-0.5,y-0.5 / math.sqrt(3)),
                 (x,y-0.5 * 2.0/math.sqrt(3)),
                 (x+0.5,y-0.5 / math.sqrt(3)),
                 (x+0.5,y+0.5 / math.sqrt(3)),
                 (x,y+0.5 * 2.0/math.sqrt(3)),
                 (x-0.5,y+0.5 / math.sqrt(3))]
            for i in range(6):
                hexV[i] = (512 + hexV[i][0]*32, 384 + hexV[i][1]*32)
            
            pygame.draw.polygon(surface, C,
                tuple(hexV))
            pygame.draw.polygon(surface, (0,0,0),
                tuple(hexV), 1)
            
        for B in self.bees:
            h,i,j = B.pos
            x,y = getHexToXY(h,i,j)
            pygame.draw.circle(surface, (255,144,128), (int(512 + 32*x),int(384 + 32*y)), 4)
            