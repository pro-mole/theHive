'''BEE module
Codifies BEEs, our main game agent'''

class BEE:
    
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
    
    '''State: what is this BEE doing now?'''
    state = "IDLE"

    '''Create a BEE at position (H,I,J), associated with world W'''
    def __init__(self,h,i,j,W):
        pos = (h,i,j)
        world = W
    
    def __repr__(self):
        R = "BEE {0} at ({1[0]},{1[1]},{1[2]})\n".format(id(self), self.pos)
        R += "HUNGER: {0}   ENERGY: {1}".format(self.hunger, self.energy)
        return R