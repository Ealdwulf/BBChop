import numbers

# standard beta function
def Beta(x,y):
    return (Gamma(x)*Gamma(y)+0.0)/Gamma(x+y)

# Standard gamma funtion, but only works on integers, which is all I need.
def Gamma(x):
    if(x==0):
        raise "Gamma called on zero!"
    if(x==1):
        return 1
    return fact(x-1)

# standard factorial function

factMemo=[numbers.const('1')]


def fact(x):
    while(x>=len(factMemo)):
        factMemo.append(factMemo[-1]*len(factMemo))
    return factMemo[x]


def choice(n,k):
    return fact(n)/fact(n-k)/fact(k)


##test functions
def binD(k,n,p):
    return nD(k,n,p)*float(choice(n,k))

def nD(k,n,p):
    return numbers.pow(p,k)*numbers.pow(1-p,n-k)

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
    return [numbers.pow(x,p) for x in l]
