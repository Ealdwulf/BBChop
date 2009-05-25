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
import sys

import likelihoods
import copy
import random
import randomdag
import dag
from listUtils import cond,listOr
import numbers

class struct:
    def __init__(self,**kwargs):
        for (key,val) in kwargs.items():
            self.__dict__[key] = val

    


single=       struct(likelihoodObj=likelihoods.singleRateCalc,   multi=False, falsePos=False,falseNeg=True)
multi=        struct(likelihoodObj=likelihoods.multiRateCalc,    multi=True,  falsePos=False,falseNeg=True)
deterministic=struct(likelihoodObj=likelihoods.deterministicCalc,multi=False, falsePos=False,falseNeg=False)



likList=[single,multi,deterministic]
def entropyTestCases():
    for randomDag in [False,True]:
        for lik in likList:
            res=copy.copy(lik)
            res.randomDag=randomDag
            res.maxCount=10
            yield res
            if res.likelihoodObj is deterministic:
                res.maxCount=1
                yield res


        
def BBChopTestCases():
    for randomDag in [False,True]:
        for lik in likList:
            res=copy.copy(lik)
            res.randomDag=randomDag
            yield res


def runTests(testFunc,casesFunc):
    
    fail=False

        
    if len(sys.argv)==1:
        
    #    for (l1,l2,falsePos,falseNeg,maxCount,randomDag) in testTab:
        for case in casesFunc():
            tfail= testFunc(case)
            fail=fail or tfail 
            if fail:
                print "->FAILED"
            else:
                print "->PASSED"

    else:
        testNum=int(sys.argv[1])
        testTab=[t for t in  casesFunc()]
        case=testTab[testNum]
        tfail=  testFunc(case)
    
        fail=fail or tfail 
    
    
    if fail:
        print "FAILED!"
        sys.exit(1)
    else:
        print "PASSED!"
        sys.exit(0)





def testDag(N,randomDag=False):
    if randomDag:
        d=randomdag.randomdag(N)
    else:
        d=dag.listDagObj
    return d

def randomEntropyData(seed,N,dag,falsePos=False,falseNeg=False,maxCount=10):
    random.seed(seed)
        
    loc=random.randint(0,N-1)
    
    locList=[False for x in range(N)]
    locList[loc]=True

    detectable=listOr(dag.anyUpto(locList),locList)
        


    counts=[(random.randint(0,maxCount),random.randint(0,maxCount)) for x in range(N)]

    # eliminate impossible counts for this test
    if not falsePos:
        counts=[ cond(not detectable[x],(counts[x][0],0),counts[x])  for x in range(N)]
    if not falseNeg:
        counts=[ cond(detectable[x],(0,counts[x][1]),counts[x])  for x in range(N)]

    UlocPrior=[random.random() for x in range(N)]
    norm=sum(UlocPrior)
    locPrior=[numbers.const(i/norm) for i in UlocPrior]
    
    return (counts,locPrior)

