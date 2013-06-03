'''Math module

Some functions and constants we'll be needing'''

import math

'''Get center XY coordinates for a Hex

X,Y are normalized, i.e., are defined in term of tile width'''
def getHexToXY(h,i,j):
    #H coordinate is just horizontal
    x = h
    #I and J is top left and right, respectively
    y = i * math.sin(math.pi/3)
    y += j * math.sin(math.pi/3)
    x += -i * math.cos(math.pi/3)
    x += j * math.cos(math.pi/3)
    return x, y

'''Get hex coordinates for X,Y position'''
def getXYToHex(x,y):
    #Again, H is simple
    H = x
    I = (y - 2 *(x - H))/2.0
    J = y - I
    #Get the normalized hex
    return normalHex(H,I,J)

'''Normalize Hex coordinates'''
def normalHex(h,i,j):
    _h,_i,_j = h,i,j
    if h == 0:
        delta = min(abs(i), abs(j))
        if i < 0 and j > 0:
            _h += delta
            _i += delta
            _j -= delta
        elif i > 0 and j < 0:
            _h -= delta
            _i -= delta
            _j += delta
    elif i == 0:
        delta = min(abs(h), abs(j))
        if h < 0 and j > 0:
            _h += delta
            _i += delta
            _j -= delta
        elif h > 0 and j < 0:
            _h -= delta
            _i -= delta
            _j += delta
    elif j == 0:
        delta = min(abs(h),abs(i))
        if h > 0 and i > 0:
            _h -= delta
            _i -= delta
            _j += delta
        elif h < 0 and i < 0:
            _h += delta
            _i += delta
            _j -= delta
    else:
        delta = min(abs(i), abs(j))
        if i > 0 and j < 0:
            _h -= delta
            _i -= delta
            _j += delta
        elif j > 0 and i < 0:
            _h += delta
            _i += delta
            _j -= delta 
    
    return _h,_i,_j