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

from listUtils import *
from evidence import entropiesFast 
import numbers
import copy
#import plot

debug=False
#debug=True



############ ABBREVIATIONS
#
#
#   E   :    Evidence
#   L   :    Location
#   d   :    number of detections at location
#   t   :    number of non-detections at location
#
#

#stratgies


# greedy strategy: always choose the location where the expected gain in entropy
# for the next observation is highest, ie, the expected entropy after the 
#next observation is smallest.

def greedyStrat(counts,locPrior,likelihoodsObj,dag):
    (currEntropy,entropyResults,findProbs)=entropiesFast(counts,locPrior,likelihoodsObj,dag)
    # test where expected entropy is smallest
            
    (next,nextp)=findMin(entropyResults)

    return next

# nearly greedy strategy: like greedy, but if we have a detection, see if observinf there again
# would be expected to improve next gain in entropy.

def nearlyGreedyStrat(counts,locPrior,likelihoodsObj,dag):
    dlocs=[i for i in range(len(counts)) if counts[i][1]]
    (currEntropy,entropyResults,findProbs)=entropiesFast(counts,locPrior,likelihoodsObj,dag)
    (next,nextE)=findMin(entropyResults)
    if len(dlocs):
        # if there is a detection, calculate the expected entropy after making another observation
        # there and then making a 'greedy' observation.
        dloc=dlocs[-1]
        (t,d)=counts[dloc]
        dcounts=copy.copy(counts)
        tcounts=copy.copy(counts)
        dcounts[dloc]=(t,d+1)
        tcounts[dloc]=(t+1,d)
        (currEntropyD,entropyResultsD,findProbsD)=entropiesFast(dcounts,locPrior,likelihoodsObj,dag)
        (currEntropyT,entropyResultsT,findProbsT)=entropiesFast(tcounts,locPrior,likelihoodsObj,dag)
        (nextD,nextED)=findMin(entropyResultsD)
        (nextT,nextET)=findMin(entropyResultsT)
        
        expectedEntropy=findProbs[dloc]*nextED+(1-findProbs[dloc])*nextET

#        print "c %1.2f n %1.02f c-n %1.04f c-e %1.04f fp %1.02f nf %1.02f nt %1.02f" %(currEntropy,nextE,currEntropy-nextE,currEntropy-expectedEntropy,findProbs[dloc],nextED,nextET)
        if (currEntropy-nextE)<(currEntropy-expectedEntropy)/2.0:
            return dloc
        else:
            return next

    else:
        return next
    




class BBChop:
    def __init__(self,locPrior,certainty,interactor,likelihoodsObj,dag,strategy=greedyStrat):

        
        self.locPrior=copy.copy(locPrior)
        self.certainty=certainty
        self.counts=[(0,0) for p in locPrior]
        self.interactor=interactor
        self.total=0
        self.likelihoodsObj=likelihoodsObj
        self.dag=dag
        self.strategy=strategy


    def addPriorKnowlege(self,positives,negatives):
        (t,d)=self.counts[-1]
        t+=negatives
        d+=positives
        self.counts[-1]=(t,d)
        

    def addResult(self,location,observation):
        (t,d)=self.counts[location]
        
        # 'None' means we've decided that this location is invalid (eg, won't compile)
        if observation is None:
            self.locPrior[location]=numbers.const(0)            
        elif observation is True:
            self.counts[location]=(t,d+1)
        else:
            self.counts[location]=(t+1,d)
            
        if debug:
            print "ct",self.counts
        

    def search(self):
        (locProbs,evProb)=self.likelihoodsObj.probs(self.counts,self.locPrior,self.dag)

        (whereabouts,maxp) = findMax(locProbs)
        if debug:
            print "lp",map(float,locProbs)
            print "ct",self.counts
        while(maxp<self.certainty):
            #decide where to seach next

            self.interactor.statusCallback(False,whereabouts,maxp,locProbs,self.counts)
                
            next=self.strategy(self.counts,self.locPrior,self.likelihoodsObj,self.dag)


            observation=self.interactor.test(next)
            self.total+=1


            # update evidence
            self.addResult(next,observation)


            (locProbs,evProb)=self.likelihoodsObj.probs(self.counts,self.locPrior,self.dag)


            if debug:
                print "lp",map(float,locProbs)
                print "e",float(entropy(locProbs)),map(float,entropyResults)
                print "fp",map(float,findProbs)
                
            (whereabouts,maxp) = findMax(locProbs)

        self.interactor.statusCallback(True,whereabouts,maxp,locProbs,self.counts)

                


        return whereabouts





