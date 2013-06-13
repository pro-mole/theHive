'''Math module

Some functions and constants we'll be needing'''

import math
import operator

'''Constants'''
'''Unitary hex vectors'''
vectorhex1 = [(0,0,1),(0,1,0),(1,0,0),(-1,0,0),(0,-1,0),(0,0,-1)]

'''Get center XY coordinates for a Hex

X,Y are normalized, i.e., are defined in term of tile width'''
def getHexToXY(h,i,j):
    #H coordinate is just horizontal
    x = h
    #I and J is top left and right, respectively
    y = i * math.sin(math.pi/3)
    y -= j * math.sin(math.pi/3)
    x += -i * math.cos(math.pi/3)
    x -= j * math.cos(math.pi/3)
    return x, y

'''Get hex coordinates for X,Y position'''
def getXYToHex(x,y):
    #Again, H is simple
    H = x
    I = (y - 2 *(x - H))/2.0
    J = - y + I
    #Get the normalized hex
    return normalHex(H,I,J)

'''Sign function; Because Python apparently can't handle it. Ok'''
'''Returns 1,0 or -1, depending on the number's sign'''
def sign(I):
    if I == 0: return 0
    return I/abs(I)
    
'''Normalization map
To reduce computation costs(I hope)'''
normalmap = {}

'''Normalize Hex coordinates'''
def normalHex(h,i,j):
    #Redefining the H-,I- and J-axis, we have that each two axis summed results in the other one negated
    #Thus: (1,1,1) = (0,0,0), and this makes things so much easy :D
    #Vector magnitudes
    H,I,J = tuple(map(abs,(h,i,j)))
    #Vector directions
    _h,_i,_j = tuple(map(sign,(h,i,j)))
    
    #Wild guess
    if abs(_h + _i + _j) <= 1 and abs(_h)+abs(_i)+abs(_j) < 3:
        return h,i,j
    
    #First case, mapping back to zero
    if _h == _i and _i == _j:
        delta = min(H,I,J)
        delta *= -_h
        h,i,j = tuple(map(operator.add,(h,i,j),(delta,delta,delta)))
        return normalHex(h,i,j)
    
    #After the first case is done with, at least ONE of the coordinates will be 0
    #Let's see who
    if _i == _j:
        delta = min(I,J)
        delta *= -_i
        h,i,j = tuple(map(operator.add,(h,i,j),(delta,delta,delta)))
        return normalHex(h,i,j)
    
    if _h == _j:
        delta = min(H,J)
        delta *= -_h
        h,i,j = tuple(map(operator.add,(h,i,j),(delta,delta,delta)))
        return normalHex(h,i,j)
        
    if _h == _i:
        delta = min(H,I)
        delta *= -_h
        h,i,j = tuple(map(operator.add,(h,i,j),(delta,delta,delta)))
        return normalHex(h,i,j)
    
    #Last case, no zeroes but 
    
    #Whatever, really
    return h,i,j