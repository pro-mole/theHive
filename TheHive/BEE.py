'''BEE module
Codifies BEEs, our main game agent'''

has_pygame = True

from HiveMath import *
import random
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
    
    '''Home hive comb'''
    home = None

    '''AI parameters'''
    '''Function: what does this BEE do?'''
    function = "WORKER"
    '''State: what is this BEE doing now?'''
    state = "IDLE"
    '''Hex Map: this is what this BEE knows about the external world; it varies from BEE to BEE'''
    hexmap = None

    '''Create a BEE at position (H,I,J), associated with world W'''
    def __init__(self,h,i,j,W,home):
        self.pos = (h,i,j)
        self.world = W
        self.home = home
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
        
        x = x*32 + 512
        y = y*32 + 384
        
        pygame.draw.circle(surface, (255,192,128), (int(x),int(y)), 4)
        pygame.draw.circle(surface, (0,0,0), (int(x),int(y)), 4, 1)
        
    def update(self):
        #Act according to state
        if self.state == "IDLE":
            if self.function == "WORKER":
                if random.random() < 0.1:
                    self.state = "ROAM"
        elif self.state == "ROAM":
            explore = False
            count = 10
            while not explore and count > 0:
                dir = random.choice(vectorhex1)
                nextPos = tuple(map(operator.add,self.pos,dir))
                explore = nextPos in self.hexmap.keys() and hexDist(nextPos,self.home) <= 12
                if explore:
                    self.pos = nextPos
            self.energy -= 1
            self.hunger += 1
        elif self.state == "MARK":
            delta = tuple(map(operator.sub,self.pos,self.home))
            H = self.world.getHex(self.pos[0],self.pos[1],self.pos[2])
            H.changeSmell("FlowerPath",1.0)
            if delta[0] != 0:
                signal = delta[0]/abs(delta[0])
                self.pos = tuple(map(operator.add,self.pos,(signal,0,0)))
            elif delta[1] != 0:
                signal = delta[1]/abs(delta[1])
                self.pos = tuple(map(operator.add,self.pos,(0,signal,0)))
            elif delta[2] != 0:
                signal = delta[2]/abs(delta[2])
                self.pos = tuple(map(operator.add,self.pos,(0,0,signal)))
            else:
                self.state = IDLE
        
        #Act according to the current Hex
        H = self.world.getHex(self.pos[0],self.pos[1],self.pos[2])
        if H.terrain == 'Flower':
            self.state = 'MARK' 
        
        #Metabolism
        self.energy -= 1
        
        #Reveal all hexes around yourself
        h,i,j = self.pos
        h,i,j = normalHex(h,i,j)
        self.pos = h,i,j
        if not (h,i,j) in self.hexmap:
            self.hexmap[(h,i,j)] = self.world.getHex(h,i,j)
            self.world.visiblehexmap[(h,i,j)] = self.world.getHex(h,i,j)
        for _H in vectorhex1:
            _h,_i,_j = tuple(map(operator.add, (h,i,j),_H))
            if not normalHex(_h,_i,_j) in self.hexmap:
                self.hexmap[normalHex(_h,_i,_j)] = self.world.getHex(_h,_i,_j)
                self.world.visiblehexmap[(_h,_i,_j)] = self.world.getHex(_h,_i,_j)