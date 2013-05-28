'''Randomization modules

Guarantee that, for the same world Seed, we'll have the same world generation'''

import random

seed = 0

'''Return seed value for Hex at position (H,I,J)'''
def getSeedForHex(pos):
    random.seed(seed)
    random.seed(random.random() + pos[0])
    random.seed(random.random() + pos[1])
    random.seed(random.random() + pos[2])
    
    return random.random()