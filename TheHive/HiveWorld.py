'''World module
codified how the world that this game happens in works'''

from BEE import *

class World:

    '''Random seed. Really, REALLY important'''
    SEED = 0;
    
    '''The Hex Map is a map of a hex data list(smells, liquids, solids, terrain) to (H,I,J) positions'''
    hexmap = {}
    
    '''BEEs. We'll keep them all together for easy of use'''
    bees = []
    
    '''Create world loading all data necessary'''
    def __init__(self,*data):
        #No data; start over
        if len(data) == 0:
            self.hexmap[(0,0,0)] = []
            self.bees.append(BEE(0,0,0,self))
            
    def __repr__(self):
        R = ""
        R += "TheHive World Object\n"
        R += "Loaded hexes: {0}\n".format(len(self.hexmap))
        R += "BEEs: \n"
        for B in self.bees:
            R += " {0};\n".format(B)
        
        return R