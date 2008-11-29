import operator
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
    return reduce(operator.mul,l,1.0)

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
