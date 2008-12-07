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
import BBChop
import random
import pdb
import likelihoods
import dag
import testCases
import randomdag

from testDetector import detect

random.seed(1)

N=10
prior=[ 1/float(N) for i in range(N)]
cert=0.9

trials=50

def testChop(likelihoodObj,dagObj,falseNeg,multi):
    tests=0
    right=0
    wrong=[]
    totalLooks=0.0
    
    for k in range(trials):
        random.seed(k+1)
        if falseNeg:
            rate=random.random()
        else:
            rate=1
        tester=detect(N,rate,dagObj,multi)
        finder=BBChop.BBChop(prior,cert,tester,likelihoodObj,dagObj)
        
        loc=tester.loc
        guess=finder.search()
    
        totalLooks+=finder.total
    
        
        tests+=tester.tests
        if(loc==guess):
            right=right+1
        else:
            wrong.append(guess)
    
        #if((k+1)%10 == 0):
        print "right%=",100.0*right/(k+1),"right=",loc==guess,"totallooks=",totalLooks/(k+1),"looks=",finder.total,"rate=",rate
            
        #if((k+1)%100 ==0):
        #   tester.printLocs()
	
    print "right:",right," out of",trials,tests/trials
    return (right/trials)<cert

def testFunc(case):
    print "testing " ,case.likelihoodObj.name(),"randomDag=",case.randomDag
    
    d=testCases.testDag(N,case.randomDag)
    return testChop(case.likelihoodObj,d,case.falseNeg,case.multi)






testCases.runTests(testFunc,testCases.BBChopTestCases)
