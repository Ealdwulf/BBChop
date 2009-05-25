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

import copy
import entropy
import numbers
import dag
from miscMath import powList
from likelihoods import Impossible
# compute the probability distribution of bug locations

# inputs:
#         counts (list[N] of tuples (ti,di))
#         locPrior (list[k<N] of prior probabilities that the bug occurs at locations k..(N-1)
#
# output list[k<N] of probabilities

debug=False


def entropies(counts,locPrior,likelihoodsObj,dag):
    (locProbs,evProb)=likelihoodsObj.probs(counts,locPrior,dag)
    deb_ef=[]
    deb_enf=[]
    findProbs=[]
    entropyResults=[]
    entropyFunc=entropy.renyi
    currEntropy=entropyFunc(locProbs)

    if debug: print "ac",counts

    for i in range(len(locProbs)):
        testFound=copy.copy(counts)
        testNotFound=copy.copy(counts)
        
        (t,d)=counts[i]
        testFound[i]=(t,d+1)
        testNotFound[i]=(t+1,d)
        
        try:
            (probsIfFound,evDProb)=likelihoodsObj.probs(testFound,locPrior,dag)
            eFound=entropyFunc(probsIfFound)
        except Impossible:
            eFound=numbers.zero
            evDProb=numbers.zero
        
        try:
            (probsIfNotFound,junk)=likelihoodsObj.probs(testNotFound,locPrior,dag)
            eNotFound=entropyFunc(probsIfNotFound)
        except Impossible:
            eNotFound=numbers.zero
        
        # probability of finding at i:
        
        findProb=evDProb/evProb
        findProbs.append(findProb)
        if debug: print "a",eFound,eNotFound,evDProb,probsIfFound
        
        # expected entropy after testing at i:
        
        eResult=eFound*findProb+eNotFound*(numbers.const(1)-findProb)
        
        entropyResults.append(eResult)

    return (currEntropy,entropyResults,findProbs)



def entropiesFast(counts,locPrior,likelihoodsObj,d):

#    d=dag.linearTestDag(len(locPrior))

    one=numbers.const(1.0)
    renyiFactor=one/(one-entropy.alpha)

    lk=likelihoodsObj.calc(counts,locPrior,entropy.alpha,d)

    (rsum,osum)=lk.orig()
    currEntropy=rsum/numbers.pow(osum,entropy.alpha)
    currEntropy =numbers.log(currEntropy)*renyiFactor
    
    entropyResults=[]
    findProbs=[]


    for i in range(len(locPrior)): 

        (findProb,renyLksFoundTot,renyLksNFoundTot,evDProb,NfoundNorm)=lk[i]
        findProbs.append(findProb)
        #entropyFound:normalise
        try: 
            eFound=renyLksFoundTot/numbers.pow(evDProb,entropy.alpha)
            
            eFound=numbers.log(eFound)*renyiFactor
        except numbers.zeroDivisionError:
            eFound=0
        except numbers.overflowError:
            eFound=0


        #entropyNotFound:normalise
        try:
            eNotFound=renyLksNFoundTot/numbers.pow(NfoundNorm,entropy.alpha)            
            eNotFound=numbers.log(eNotFound)*renyiFactor
        except numbers.zeroDivisionError:
            eNotFound=0
        except numbers.overflowError:
            eNotFound=0

        # expected entropy after testing at i:
        if debug: print "b",eFound,eNotFound,findProb
        
        eResult=eFound*findProb+eNotFound*(1-findProb)
        
        entropyResults.append(eResult)

    return (currEntropy,entropyResults,findProbs)
