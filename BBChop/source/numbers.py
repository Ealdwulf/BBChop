#    Copyright 2008 Ealdwulf Wuffinga

#    This file is part of BBChop.
#
#    BBChop is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    BBChop is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with BBChop.  If not, see <http://www.gnu.org/licenses/>.

# define what kind of number object to use

numberType = 'float'
#numberType = 'mpmath'

import math


if numberType == 'mpmath':
    import mpmath
    mpmath.mp.prec=200

    def const(str):
        return mpmath.mpf(str)

    power=mpmath.power

elif numberType == 'float':
    
    def const(str):
        return float(str)
    
    power=math.pow

else:
    raise "numberType set incorrectly\n"


def log(x):
    return math.log(x)

def exp(x):
    return math.exp(x)

def pow(a,b):
    if a==0:
        return 0
    else:
        return power(a,b)

