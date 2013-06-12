'''BEE module
Codifies BEEs, our main game agent'''

has_pygame = True

from HiveMath import *
import operator
try:
    import pygame
    from pygame.locals import *
except ImportError:
    has_pygame = False

class BEE:
    '''Statics'''
    '''Enumerations'''
    enumFunction = ["WORKER", "QUEEN", "SOLDIER"]
    enumSkill = ["HONEYMAKE","HIVEBUILD", "EGGLAY", "EGGTEND", "QUEENTEND", "FOODFIND", "SCOUT"]
    enumState = ["IDLE","ROAM","REST","FEED","INSPECT"]
    
    '''Position'''
    pos = (0,0,0)
    '''Associated World'''
    world = None
    '''Cargo'''
    cargo = []
    '''Hunger'''
    hunger = 0
    '''Energy'''
    energy = 1000

    '''AI parameters'''
    '''Function: what does this BEE do?'''
    function = "WORKER"
    '''State: what is this BEE doing now?'''
    state = "IDLE"
    '''Hex Map: this is what this BEE knows about the external world; it varies from BEE to BEE'''
    hexmap = None

    '''Create a BEE at position (H,I,J), associated with world W'''
    def __init__(self,h,i,j,W):
        self.pos = (h,i,j)
        self.world = W
        self.hexmap = {}
        self.update()
    
    def __repr__(self):
        R = "BEE {0} at ({1[0]},{1[1]},{1[2]})\n".format(id(self), self.pos)
        R += "HUNGER: {0}   ENERGY: {1}".format(self.hunger, self.energy)
        return R
    
    def setFunction(self, function):
        if function in self.enumFunction:
            self.function = function
    
    def setState(self, state):
        #There'll be a whole hodge podge of valid transitions here. For the time being, just do it
        if state in self.enumState:
            self.state = state
    
    def draw(self, surface):
        h,i,j = self.pos
        x,y = getHexToXY(h,i,j)
        
        pygame.draw.circle(surface, (255,192,128), (x,y))
        
    def update(self):
        #Reveal all hexes around yourself
        h,i,j = self.pos
        h,i,j = normalHex(h,i,j)
        if not (h,i,j) in self.hexmap:
            self.hexmap[(h,i,j)] = self.world.getHex(h,i,j)
            self.world.visiblehexmap[(h,i,j)] = self.world.getHex(h,i,j)
        for _H in vectorhex1:
            _h,_i,_j = tuple(map(operator.add, (h,i,j),_H))
            if not normalHex(_h,_i,_j) in self.hexmap:
                self.hexmap[normalHex(_h,_i,_j)] = self.world.getHex(_h,_i,_j)
                self.world.visiblehexmap[(_h,_i,_j)] = self.world.getHex(_h,_i,_j)