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

import numberType

# standard beta function



# flag to determine whether to use the dumb version or log-space version.
useLogFact=1

# log-space version
def BetaX(x,y):
    return numberType.exp(logGamma(x)+logGamma(y)-logGamma(x+y))

# dumb version (subexpressions are huge)
def BetaY(x,y):
    return (Gamma(x)*Gamma(y)+0.0)/Gamma(x+y)


if useLogFact:
    Beta=BetaX
else:
    Beta=BetaY


# Standard gamma function, but only works on integers, which is all I need.
def Gamma(x):
    if(x==0):
        raise "Gamma called on zero!"
    if(x==1):
        return 1
    return fact(x-1)



# logGamma
def logGamma(x):
    if(x==0):
        raise "Gamma called on zero!"
    if(x==1):
        return 0
    return logFact(x-1)

# standard factorial function

factMemo=[numberType.const('1')]

# standard factorial function
def fact(x):
    while(x>=len(factMemo)):
        factMemo.append(factMemo[-1]*len(factMemo))
    return factMemo[x]

# log-factorial function

logFactMemo=[numberType.const('0')]

def logFact(x):
    while(x>=len(logFactMemo)):
        logFactMemo.append(logFactMemo[-1]+numberType.log(len(logFactMemo)))
    return logFactMemo[x]


def choice(n,k):
    return fact(n)/fact(n-k)/fact(k)


##test functions
def binD(k,n,p):
    return nD(k,n,p)*float(choice(n,k))

def nD(k,n,p):
    return numberType.pow(p,k)*numberType.pow(1-p,n-k)

def pe(f,ds,ts,r,i):
    dx=sum(ds[:i])
    if dx>0:
        return 0
    p=1.0
    for x in range(i,len(ds)):
        p=p*f(ds[x],ds[x]+ts[x],r) 
    return p
    
        
#FIXME why is t1(nD)==t1(binD)?
def t1(f,ds,ts,r):
    pl=[pe(f,ds,ts,r,x) for x in range(len(ds))]
    pt=sum(pl)
    return [pl[x]/pt for x in range(len(ds))]
    

def powList(l,p):
    return [numberType.pow(x,p) for x in l]
