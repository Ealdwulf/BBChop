import mpmath
import math
mpmath.mp.prec=200
def const(str):
    return mpmath.mpf(str)

import pdb
def log(x):
    return math.log(x)


def pow(a,b):
    if a==0:
        return 0
    else:
        return mpmath.power(a,b)
