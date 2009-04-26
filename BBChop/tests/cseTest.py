import random
import cse
import sys

if True:
    numVals=98
    numExps=99
    numTests=100
else:
    numVals=10
    numExps=2
    numTests=10


def union(args):
    res=set()
    for a in args:
        res=res.union(a)
    return res
    

def randomExp(pop):
    sw=random.randint(0,2)
    if sw==0:
        return set([])
    elif sw==1:
        max=5
    elif sw==2:
        max=len(pop)

    num=random.randint(0,max)

    exp=set(random.sample(pop,num))
    return exp
    
fail=False


for i in range(numTests):
    random.seed(i)
    pop=range(numVals)
    vals=[set([v]) for v in pop]
    
    explist=[randomExp(pop) for k in range(numExps)]

    
    tcse=cse.CommonSubExpressions(numVals)

    expl=tcse.getExpList(explist)

    res=expl.doCalc(vals,union,set())

    print "test %d " % i,
    
    if res!=explist:
        print "fail"
        fail=True
    else:
        print "pass"

if fail:
    print "FAILED"
    sys.exit(1)
else:
    print "PASSED"
    sys.exit(0)
    
