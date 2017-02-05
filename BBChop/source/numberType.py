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


# use mpmath if available, because it's 10x faster than decimal.
try:
    import mpmath
    numberType = 'mpmath'
except ImportError:
    import decimal    
    numberType = 'Decimal'


#numberType = 'float'

import math
import copy



if numberType == 'mpmath':
    mpmath.mp.prec=200

    def const(str):
        return mpmath.mpf(str)

    power=mpmath.power
    log=math.log
    exp=math.exp
    copyList=copy.copy
    zeroDivisionError=ZeroDivisionError
    overflowError=OverflowError
    inf = mpmath.inf

elif numberType == 'float':
    
    def const(str):
        return float(str)
    
    power=math.pow
    log=math.log
    exp=math.exp
    copyList=copy.copy
    zeroDivisionError=ZeroDivisionError
    overflowError=OverflowError
    inf = float('inf')

elif numberType == 'Decimal':
    c=decimal.getcontext()
    c.prec=60

    def const(x):
        return decimal.Decimal(str(x))

    def power(a,b):
        return a**b

    def log(x):
        return const(math.log(x))

    def exp(x):
        return const(math.exp(x))

    def copyList(l):
        return [const(x) for x in l]

    zeroDivisionError=ZeroDivisionError
    overflowError=decimal.InvalidOperation
    inf = decimal.Decimal('inf')




else:
    raise "numberType set incorrectly\n"



def pow(a,b):
    if a==0:
        return 0
    else:
        return power(a,b)

zero=const(0)
one=const(1)
