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

import operator
import numbers
# returns (index,min)
def findMin(alist):
    p=1000000000000
    w=0
    for i in range(len(alist)):
        if alist[i]<p:
            w=i
            p=alist[i]
    return (w,p)
# returns (index,max)
def findMax(alist):
    p=0
    w=0
    for i in range(len(alist)):
        if alist[i]>p:
            w=i
            p=alist[i]
    return (w,p)

def listComb(comb,*args):
    r=range(len(args[0]))
    
    return [comb([arg[i] for arg in args]) for i in r]

def listComb1(op,comb,first,*args):
    r=range(len(args[0]))
    
    return [op(first[i],comb([arg[i] for arg in args])) for i in r]

listAdd=lambda *vals: listComb(sum,*vals)
listSub=lambda *vals: listComb1(operator.sub,sum,*vals)


def prod(l):
    return reduce(operator.mul,l,numbers.const(1.0))

listAnd=lambda *vals: listComb(all,*vals)
listOr =lambda *vals: listComb(any,*vals)

listMul=lambda *vals: listComb(prod,*vals)
listDiv=lambda *vals: listComb1(operator.div,prod,*vals)


def cond(c,a,b):
    if c:
        return a
    else:
        return b

def listCond(c,a,b):
    return [cond(c[i],a[i],b[i]) for i in range(len(c))]
