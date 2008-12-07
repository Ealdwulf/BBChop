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
import sys
import math
import time
import copy
import os
from testDetector import detect
import statDb

from analysisRanges import *





trials=1000
maxLen=5000




def makeStat(seed,rate=None,minRate=None,maxRate=None,N=None,prior=None,cert=None,likelihoodObj=None,dagObj=None,counts=None):
    

    if rate is None:
        if minRate is None:
            minRate=0.0
        if maxRate is None:
            maxRate=1.0
        rate=random.uniform(minRate,maxRate)

    if N is None:
        N=random.randint(2,maxLen)
    if prior is None:
        prior=[ 1/float(N) for i in range(N)]

    if cert is None:
        db=random.uniform(3,6)
        cert=1.0-pow(0.5,db)

    if dagObj is None:
        dagObj=dag.listDagObj


    tester=detect(N,rate,dagObj,dagObj is likelihoods.multiRateCalc)
    finder=BBChop.BBChop(prior,cert,tester,likelihoodObj,dagObj)
    
    loc=tester.loc
    if counts is not None:
        finder.restoreCheckpoint(prior,copy.copy(counts))
    
    key=(rate,loc,N,cert,counts[-1][0],counts[-1][1],likelihoodObj.name().strip(),seed)
    if statDb.has_key(key):
        (tests,guess,right)=statDb.get(key)
        sys.stdout.write('.')
        sys.stdout.flush()
        
    else:
        guess=finder.search()
        right=(loc==guess)
        tests=tester.tests
        sys.stdout.write('#')
        sys.stdout.flush()
        statDb.add(key,(tests,guess,right))


    return (rate,loc,N,cert,tests,guess,right,likelihoodObj.name(),counts[-1])



class getAvgTests:
    def __init__(self,limit,**kwargs):
        self.kwargs=kwargs
        self.tot=0.0
        self.totSq=0.0
        self.num=0.0
        self.limit=limit
        self.avg=0
        self.sd=10
        self.seed=1

    def next(self):
        random.seed(self.seed)
        self.seed+=1
        (rate,loc,N,cert,tests,guess,right,lname,lastcount)=makeStat(self.seed,**self.kwargs)
        self.tot+=tests
        self.totSq+=tests*tests
        self.num+=1
        self.avg=self.tot/self.num

        self.sd=math.sqrt(self.totSq/self.num-self.avg*self.avg)
        #print self.avg,self.sd
        return (self.sd/self.num>=(self.avg/self.limit)) or (self.num<5)

    def stats(self):
         return (self.avg,self.sd)



#import pdb
#pdb.set_trace()

def makeStats(NRange,rateCountList,certRange,each,likelihoodObjs):
    for likelihoodObj in likelihoodObjs:
        for Nval in  NRange: #[10, 20, 50, 100, 200, 500, 1000]:

            for (lastCount,rate) in rateCountList:
                counts=[(0,0) for i in range(Nval)]
                counts[-1]=lastCount

                start=time.clock()
                for certVal in certRange:
                    
                    a=getAvgTests(5,N=Nval,rate=rate,cert=certVal,likelihoodObj=likelihoodObj,counts=counts)
                    
                    for i in range(each):
                        a.next()
                    print
                    
           
                print "took",time.clock()-start,"seconds"
                    


lks=          [likelihoods.singleRateCalc,likelihoods.multiRateCalc]

statDb.open()


makeStats(standardN, rateCountZ,   standardCert,100,lks)
makeStats(standardN, rateCountV,   standardCert,100,lks[:1])
makeStats(steppedN,  rateCountHalf,standardCert,100,lks[:1])
makeStats(logN,  rateCountHalf,[0.7],200,lks[:1])


statDb.close()
