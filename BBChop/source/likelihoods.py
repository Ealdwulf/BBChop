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
from miscMath import Beta,fact,choice,powList
from listUtils import *

debug=False

# exception to raise when asked to calculate a probability distribution on 'loc' given impossible evidence
class Impossible(Exception): 
    def __coerce__(self,other):
        return (type(other)(0.0),0.0)

# special object used to identify zero even though for the most part we are using floating point.

Zero=False
    

def g(pred,Ti,Di,Lprior):
    if(pred):
        return numberType.zero
    else:
        # TODO: This fails for B(638 + 1, 664 + 1).
        # With those large numbers, the result is always 0.
        # From XKCD: Have you tried Logarithms?
        # betaln(z,w) = gammaln(z)+gammaln(w)-gammaln(z+w)
        
        #print(pred, Ti, Di, Lprior, Beta(Di+1,Ti+1)*Lprior)
        
        return Beta(Di+1,Ti+1)*Lprior
    
def probsFromLikelihoods(likelihoods,likelihoodTot):
    #normalise locProbs
    probs=[]

    if all([l is Zero for l in likelihoods]):
        raise Impossible
    
    for li in likelihoods :
        probs.append(li/likelihoodTot)
    return probs
        
# returns a posteriori P(L|E) and a priori P(E) (that is, P(E|L) marginalised over L)
def probs(counts,locPrior,likelihoodsFunc,dag,doprint=None):    
    (ls,lsTot,junk)=likelihoodsFunc(counts,locPrior,dag)
    if debug: print "al",ls
    if doprint!=None:
        print doprint,ls
    probs=probsFromLikelihoods(ls,lsTot)
    return (probs,lsTot)

# NB: these are not technically likelihoods, because they include the prior.

# likelihood calculation functions. 
# returns: P(counts| location)*prior(location) for each location and
# their sum. 
# Also returns P(incD(counts,location)|location))*prior(location) for each location
# and  P(incT(counts,location)|location))*prior(location) for each location
# where incD and incT increment D and T for a particular
# location by one.


# if we assume that there is a single failure rate r at all locations:

def singleRate(counts,locPrior,dag):
    # counts is a list of tuples (ti,di)

    ts=[ti for (ti,di) in counts]
    ds=[di for (ti,di) in counts]


    Ts=listAdd(ts,dag.sumAfter(ts))
    Ds=listAdd(ds,dag.sumAfter(ds))


    # calculate predicates for likelihoods 


    #if a detection has occured, only locations <= that location remain possible.
    # Therefore we eliminate locations not <= any detection, which is those
    # > or unrelated to the detection 
    preds=[di>0 for di in ds]
    predsU=dag.anyUpto(preds)
    predsO=dag.anyOther(preds)
    preds=listOr(predsU,predsO) 

    #calculate likelihoods
    gs=[]
    gsFound=[]
    gsNFound=[]
    gtot=0
    for i in xrange(len(counts)):
        gi=g(preds[i],Ts[i]  ,Ds[i]  ,locPrior[i])
        gf=g(preds[i],Ts[i]  ,Ds[i]+1,locPrior[i])
        gn=g(preds[i],Ts[i]+1,Ds[i],  locPrior[i])
        gtot+=gi
        gs.append(gi)
        gsFound.append(gf)
        gsNFound.append(gn)

    

    return (gs,gtot,(gsFound,gsNFound))

def gMulti(pred,beta,Lprior):
    if pred:
        return numberType.zero
    else:
        return beta*Lprior

#version not assuming anything about rates of failure at different locations



def multiRate(counts,locPrior,dag):
    # counts is a list of tuples (ti,di)



    # calculate predicates for likelihoods 


    ts=[ti for (ti,di) in counts]
    ds=[di for (ti,di) in counts]

    betas1=[Beta(ds[i]+1,  ts[i]+1  ) for i in xrange(len(locPrior))]
    betasF=[Beta(ds[i]+1+1,ts[i]+1  ) for i in xrange(len(locPrior))]
    betasN=[Beta(ds[i]+1,  ts[i]+1+1) for i in xrange(len(locPrior))]

    betas=dag.prodAfter(betas1)
    betas=listMul(betas,betas1)
    betasFound=listMul(betasF,betas1)
    betasNFound=listMul(betasN,betas1)

    #if a detection has occured, only locations <= that location remain possible.
    # Therefore we eliminate locations not <= any detection, which is those
    # > or unrelated to the detection 
    preds=[di>0 for di in ds]
    predsU=dag.anyUpto(preds)
    predsO=dag.anyOther(preds)
    preds=listOr(predsU,predsO) 


    #calculate likelihoods
    gs=[]
    gsFound=[]
    gsNFound=[]
    gtot=0
    for i in xrange(len(counts)):
        gi=gMulti(preds[i],betas[i],      locPrior[i])
        gtot+=gi
        gs.append(gi)


    

    return (gs,gtot,(betas1,betasF,betasN))




#enum
cOrig=0
cFound=1
cNFound=2



# in order to avoid O(N^2) when calculating the O(N) entropies each from O(N) likelihoods,
# we need to take advantage of the fact that many of the likelihoods required are the same

# likelihoodCalc is given the counts and calculates all the necessary likelihoods, sums of likelihoods,
# and sums of (likelihood ** alpha) necessary to compute the O(N) renyi entropies.

# A different implementation is required for each likelihood function, due to the different relationships
# between the likelihoods which we need to exploit.


# abstract base class: contains logic not specific to one likelihood function
class likelihoodCalc:
    def __init__(self,counts,locPrior,alpha,dag):
        self.counts=counts
        self.locPrior=locPrior
        self.dag=dag

    # returns a list of at each location, the sum of the likelihoods, or the sum
    # of the likelihoods raised to the power alpha ( if 'renyi'==True)
    # for either Found or Not Found (depending on 'whichDat')
    def calcOne(self,renyi,whichDat):
        tot=listAdd(
            self.contribSelf(renyi,whichDat),
            self.contribUpto(renyi,whichDat),
            self.contribOther(renyi,whichDat),
            self.contribAfter(renyi,whichDat))
        return tot
    
    # calculate the 4 different lists of totals, which will later be returned by __getitem__().
    def calc(self):
        
        FoundNorms=self.calcOne(False,cFound)        
        NfoundNorms=self.calcOne(False,cNFound)
        
        
        renyiLksFoundTots= self.calcOne(True,cFound)
        renyiLksNFoundTots=self.calcOne(True,cNFound)
        
        # probability of finding at i:
        findProbs=[FoundNorm/self.lksTot for FoundNorm in FoundNorms]
        

        
        self.findProbs=findProbs
        self.renyiLksFoundTots=renyiLksFoundTots
        self.renyiLksNFoundTots=renyiLksNFoundTots
        self.FoundNorms=FoundNorms
        self.NfoundNorms=NfoundNorms
        
    # return, for location i: 
    # 1. The probability of detecting at i, given the current evidence
    # 2. The sum of the likelihood (raised to alpha) that the data is at each location, given the current evidence plus
    #    one additional detection at location i.
    # 3. as 2. but for one additional *non*detection at i
    # 4. as 2. but not raised to the power alpha
    # 5. as 4.  but for one additional *non*detection at i


    def __getitem__(self,i):
        return (self.findProbs[i],
                self.renyiLksFoundTots[i],
                self.renyiLksNFoundTots[i],
                self.FoundNorms[i],
                self.NfoundNorms[i]
                )

# store different variants of data, for easy selection based on 'renyi' (if we want the data^alpha), original,
# 'found' and 'not found'

def switchDat(orig,found,Nfound,alpha):
    r={}
    r[False]=[orig,found,Nfound]
    r[True]=[powList(orig,alpha),powList(found,alpha),powList(Nfound,alpha)]
    return r

# calculations specific to singleRate prior on r.
#This class assumes 

# A1: 
# if d[i]>0 for any i and j>i, then likelihood[j]=0

# A2:
# if for two sets of evidence d1[i]==d2[i] and t1[i]==t2[i]
# except that for some j d2[j]=d1[j]+1
# then likelihood_1[k]=likelihood_2[k] for all k<j

# A3
# as A2 except  for some j t2[j]=t1[j]+1

# A4
# if for two sets of evidence d1[i]==d2[i] and t1[i]==t2[i]
# except that for some j d2[j]=d1[j]+1
# and  d2[j+1]+1=d1[j+1]
#
# Then  likelihood_1[k]=likelihood_2[k] for all k<j
# And   likelihood_1[k]=likelihood_2[k] for all k>j

# A5:
# as A4 except for t1 and t2 instead of d1 and d2.



class singleRateCalcX(likelihoodCalc):


    def __init__(self,counts,locPrior,alpha,dag):

        likelihoodCalc.__init__(self,counts,locPrior,alpha,dag)
        (lks,lksTot,(lksFound,lksNFound))=singleRate(self.counts,locPrior,self.dag)

        self.lksTot=lksTot
        self.likelihoodDat=switchDat(lks,lksFound,lksNFound,alpha)
        self.calc()

            
    def contribSelf(self,renyi,whichDat):
        return self.likelihoodDat[renyi][whichDat]

    def contribUpto(self,renyi,whichDat):
        return self.dag.sumUpto(self.likelihoodDat[renyi][whichDat])

    def contribOther(self,renyi,whichDat):
        if whichDat==cFound:
            return [numberType.zero for i in self.counts]  # if found at i, cannot be 'other to' i as we assume no false positives.
        else:
            return self.dag.sumOther(self.likelihoodDat[renyi][cOrig])

    def contribAfter(self,renyi,whichDat):
        if whichDat==cFound:
            return [numberType.zero for i in self.counts]  # if found at i, cannot be after i as we assume no false positives.
        else:
            return self.dag.sumAfter(self.likelihoodDat[renyi][cOrig])

    def orig(self):
        rsum=sum(self.likelihoodDat[True][cOrig])
        osum=sum(self.likelihoodDat[False][cOrig])
        return (rsum,osum)



# unlike the case for singleRate, all the likelihoods up to k vary when we move our observation
# location from k to k+1. But we still don't need to add them all up again, because they vary by a 
# constant factor, so we can cancel out the old and multiply by the new.

class multiRateCalcX(likelihoodCalc):


    def __init__(self,counts,locPrior,alpha,dag):

        likelihoodCalc.__init__(self,counts,locPrior,alpha,dag)
        (lks,lksTot,(betas,betasFound,betasNFound))=multiRate(self.counts,locPrior,self.dag)

        self.lksTot=lksTot
         
        self.betasDat=switchDat(betas,betasFound,betasNFound,alpha)
        self.likelihoodDat={False: lks, True: powList(lks,alpha)}

        s= listAdd(lks,dag.sumUpto(lks))
        s=listDiv(s,betas)                  # sumUpto with the beta contribution from [i] cancelled
        renyiLks=powList(lks,alpha)
        r=listAdd(renyiLks, dag.sumUpto(renyiLks))
        r=listDiv(r,self.betasDat[True][cOrig])
        self.uptoBetas = {False: s, True: r} # 
        self.calc()
        

            
    def contribSelf(self,renyi,whichDat):
        return [numberType.zero for i in self.counts] # 'self' contrib included in 'upto'

    def contribUpto(self,renyi,whichDat):
        return listMul(self.uptoBetas[renyi],self.betasDat[renyi][whichDat])


    def contribOther(self,renyi,whichDat):
        if whichDat==cFound:
            return [numberType.zero for i in self.counts]
        else:
            return self.dag.sumOther(self.likelihoodDat[renyi])

    def contribAfter(self,renyi,whichDat):
        if whichDat==cFound:
            return [numberType.zero for i in self.counts]
        else:
            return self.dag.sumAfter(self.likelihoodDat[renyi])

    def orig(self):
        rsum=sum(self.likelihoodDat[True])
        osum=sum(self.likelihoodDat[False])
        return (rsum,osum)


# simple case: no false negatives or false positives
def deterministic(counts,locPrior,dag):
    ts=[ti for (ti,di) in counts]
    ds=[di for (ti,di) in counts]

    #if a detection has occured, only locations <= the detection location remain possible.
    # Therefore we eliminate locations not <= any detection, which is those
    # > or unrelated to the detection 
    dpreds1=[di>0 for di in ds]
    dpredsU=dag.anyUpto(dpreds1)
    dpredsO=dag.anyOther(dpreds1)
    dpreds=listOr(dpredsU,dpredsO) 

    # the situation is the complement for nondetections: 
    # locations <= the detection location are eliminated.
    # but this not symmetric: we don't exclude 'other' locations.
    tpreds1=[ti>0 for ti in ts]
    tpreds=listOr(tpreds1,dag.anyAfter(tpreds1))

    preds=listOr(dpreds,tpreds)
    z=[Zero for i in counts]
    
    lks=listCond(preds,z,locPrior)

    lksTot=sum(lks)
    return (lks,lksTot,None)


class deterministicCalcX(likelihoodCalc):
    def __init__(self,counts,locPrior,alpha,dag):
        likelihoodCalc.__init__(self,counts,locPrior,alpha,dag)
        (lks,lksTot,junk)=deterministic(self.counts,locPrior,self.dag)
    
        
        self.lksTot=lksTot
        self.lksDat={False:lks,True:powList(lks,alpha)}
        self.calc()
    
    
    def contribSelf(self,renyi,whichDat):
        if whichDat==cNFound:
            return [Zero for i in self.counts] 
        else:
            return self.lksDat[renyi]


    def contribUpto(self,renyi,whichDat):
        if  whichDat==cNFound:
            return [Zero for i in self.counts] 
        else:
            return self.dag.sumUpto(self.lksDat[renyi])


    def contribOther(self,renyi,whichDat):
        if whichDat==cFound:
            return [Zero for i in self.counts]
        else:
            other= self.dag.sumOther(self.lksDat[renyi])

            # rounding error can cause this to be negative, zero to avoid upsetting math.log()
            c=[o<0 for o in other]
            zero=[numberType.zero for o in other]
            other=listCond(c,zero,other)
            return other

    def contribAfter(self,renyi,whichDat):
        if whichDat==cFound:
            return [Zero for i in self.counts]
        else:
            return self.dag.sumAfter(self.lksDat[renyi])

    def orig(self):
        rsum=sum(self.lksDat[True])
        osum=sum(self.lksDat[False])
        return (rsum,osum)

# wrapper class. Exists mainly to make the calcClass 'functional'
# IE, when counts has changed, we create a new calcClass rather than updating some state.
# There's no technical reason to do that, it just makes the code easier for me to understand.

class likelihood:
    def __init__(self,calcClass,func):
        self.calcClass=calcClass
        self.func=func
        
    def name(self):
        return self.func.func_name

    def probs(self,counts,locPrior,dag):
        return probs(counts,locPrior,self.func,dag)


    def calc(self,counts,locPrior,alpha,dag):
        return self.calcClass(counts,locPrior,alpha,dag)



singleRateCalc=likelihood(singleRateCalcX,singleRate)
multiRateCalc=likelihood(multiRateCalcX,multiRate)
deterministicCalc=likelihood(deterministicCalcX,deterministic)


