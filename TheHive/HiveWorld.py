'''World module
codified how the world that this game happens in works'''

from BEE import *
import hiveRand
import random
import math

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
    def changeLiquid(self, solid, quantity):
        if self.solids.has_key(liq):
            self.solids[solid] += quantity
        else:
            self.solids[solid] = quantity
        
        if self.solids[solid] < 0:
                self.solids.pop(liq)
    
    '''Adds powder to this Hex
    Powders cannot be smaller than 0'''
    def changeLiquid(self, powder, weight):
        if self.powders.has_key(liq):
            self.powders[powder] += weight
        else:
            self.powders[powder] = weight
        
        if self.powders[powder] < 0:
                self.powders.pop(liq)

class World:

    '''Random seed. Really, REALLY important'''
    SEED = 0;
    
    '''The Hex Map is a map of a hex data list(smells, liquids, solids, terrain) to (H,I,J) positions'''
    hexmap = {}
    
    '''BEEs. We'll keep them all together for easy of use'''
    bees = []
    
    '''All entities'''
    entities = []
    
    '''Create world loading all data necessary'''
    def __init__(self,*data):
        #No data; start over
        if len(data) == 0:
            self.hexmap[(0,0,0)] = Hex('Hive')
            initrange = 2
            for h in range(-initrange,initrange+1):
                for i in range(-initrange,initrange+1):
                    for j in range(-initrange,initrange+1):
                        self.addHex(h,i,j)
            
            B = BEE(0,0,0,self)
            self.bees.append(B)
            self.entities.append(B)
        
        hiveRand.seed = self.SEED    
            
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
        if self.hexmap.has_key((h,i,j)):
            return self.hexmap[(h,i,j)]
        else:
            return(self.addHex(h,i,j))
    
    '''Add new hex in position H,I,J(taking in account randomizations)'''
    def addHex(self,h,i,j):
        if not self.hexmap.has_key((h,i,j)):
            random.seed(hiveRand.getSeedForHex((h,i,j)))
            chance = random.random()
            #Flowers on a 1% chance
            if chance < 0.01:
                self.hexmap[(h,i,j)] = Hex('Flower')
                self.hexmap[(h,i,j)].changeLiquids('Honey',int(random.random() * 20))
                self.hexmap[(h,i,j)].changePowders('Pollen',int(random.random() * 50))
                self.hexmap[(h,i,j)].changeSmell('Flower',1)
                for d in range(1,5):
                    self.getHex(h+d,i,j).changeSmell('Flower', math.pow(2,-d))
                    self.getHex(h-d,i,j).changeSmell('Flower', math.pow(2,-d))
                    self.getHex(h,i+d,j).changeSmell('Flower', math.pow(2,-d))
                    self.getHex(h,i-d,j).changeSmell('Flower', math.pow(2,-d))
                    self.getHex(h,i,j+d).changeSmell('Flower', math.pow(2,-d))
                    self.getHex(h,i,j-d).changeSmell('Flower', math.pow(2,-d))
            #Everything else is just plain ol' dirt   
            else:
                self.hexmap[(h,i,j)] = Hex('Dirt')
        return self.hexmap[(h,i,j)]