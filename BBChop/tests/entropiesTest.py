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
import evidence
import random

import dag
import testCases
import numbers

epsilon=numbers.const(0.000000001)
epCoeff=1+epsilon
epDelta=numbers.const(0.00000000000001)



def rough_eq(a,b):
    r=True
    minS_a=a-epDelta
    maxS_a=a+epDelta
    if a<0:
        minP_a=a*epCoeff
        maxP_a=a/epCoeff
    else:
        minP_a=a/epCoeff
        maxP_a=a*epCoeff


    min_a=min(minP_a,minS_a)
    max_a=max(maxP_a,maxS_a)
        

    return (min_a<=b) and (b <=max_a)

n=10

tests=150



import pdb




def testEntropyFunc(entropyFunc1,entropyFunc2,likelihoodArg1,likelihoodArg2,falsePos=False,falseNeg=False,maxCount=10,randomDag=False):
    print "testing " ,entropyFunc1.func_name,entropyFunc2.func_name,likelihoodArg1.name(),likelihoodArg2.name(),"maxCount=",maxCount,"randomDag=",randomDag
    
    fail=False
    for t in  range(tests):

        d=testCases.testDag(n,randomDag)
        (counts,locPrior)=testCases.randomEntropyData(t+1,n,d,falsePos,falseNeg,maxCount)
        
    
#        pdb.set_trace()
        (c1,e1,f1)=entropyFunc1(counts,locPrior,likelihoodArg1,d)
    #    pdb.set_trace()
        (c2,e2,f2)=entropyFunc2(counts,locPrior,likelihoodArg2,d)
    
        thisFail=False
        if not rough_eq(c1,c2):
            print "Error:\t",c1,c2
            thisFail=True
            
        for j in range(n):
    #        print "entropy:\t ",j,e1[j],e2[j] #,max(e1[j]/e2[j],e2[j]/e1[j])
            if not rough_eq(e1[j],e2[j]):
                print "Error:\t",e1[j],e2[j]
                thisFail=True
    
        if thisFail:
            fail=True
            print "test %d failed!" % t
        else:
            print "test %d passed" % t
    if fail:
        print "FAILED!"
    else:
        print "PASSED!"

    return fail



e1=evidence.entropies
e2=evidence.entropiesFast

def testFunc(case):
    return  testEntropyFunc(e1,e2,case.likelihoodObj,case.likelihoodObj,case.falsePos,case.falseNeg,case.maxCount,case.randomDag)    


testCases.runTests(testFunc,testCases.entropyTestCases)



    
    


