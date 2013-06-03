'''Math module

Some functions and constants we'll be needing'''

import math

'''Get center XY coordinates for a Hex'''
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
    return H,I,J

'''Normalize Hex coordinates'''
def normalHex(h,i,j):
    if (i < 0 and j > 0) or (i > 0 and j < 0):
        _h = min(abs(i), abs(j))
        if i < 0:
            I = i + _h
            J = j - _h
            H = h + _h
        else:
            I = i - _h
            J = j + _h
            H = h - _h
        return (H,I,J)
    else:
        return (h,i,j)