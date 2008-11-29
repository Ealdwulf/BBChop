import BBChop
from testDetector import detect

import likelihoods
import math
from matplotlib import colors as mcolors
import dag



class logdetect(detect):
    def __init__(self,len,rate,dag,multi,loc=None,debug=False):
        detect.__init__(self,len,rate,dag,multi,loc,debug)
        
        self.probCollect=[]

    def statusCallback(self,ended,mostLikely,mostLikelyProb,probs,counts):
        
        thisProbs=[float(x) for x in probs]

        self.probCollect.append(thisProbs)


    def get_table(self):
        return array(self.probCollect)


from pylab import *
from copy import copy

def normalise(v):
    s=sum(v)
    return [x/s for x in v]
    

class gammaNorm(mcolors.Normalize):
    def __init__(self, vmin=None, vmax=None, clip = True,gamma=1.0):
        mcolors.Normalize.__init__(self,vmin,vmax,clip)
        self.gamma=gamma
    
    def __call__(self,value,clip=None):
        y= mcolors.Normalize.__call__(self,value,clip)
        return y**self.gamma

    def inverse(self,value):
        y=value**(1.0/self.gamma)
        return mcolors.Normalize.inverse(self,y)



def deterministic_chop(N,loc):
    prior=[1.0]*N
    min=0
    max=N-1

    
    res=[normalise(prior)]

    while max!=min:
        testloc=min+(max-min)/2
#        print min,max,testloc

        if testloc<loc:
            for i in range(min,testloc+1):
                prior[i]=0
            min=testloc+1
        else:
            for i in range(testloc+1,max+1):
                prior[i]=0
            max=testloc


        res.append(normalise(prior))
    return array(res)


def probabalistic_chop(N,loc):
    prior=[ 1/float(N) for i in range(N)]
    cert=0.9
    rate=0.9
    likelihoodObj=likelihoods.singleRateCalc

    tester=logdetect(N,rate,dag.listDagObj,False,loc=loc)
    finder=BBChop.BBChop(prior,cert,tester,likelihoodObj,dag.listDagObj)


    guess=finder.search()
    right=(loc==guess)
    return tester.get_table()

        
d1=deterministic_chop(64,9)
d2=probabalistic_chop(64,9)



def dsubplot(atitle,data,subp):    
    gamma=0.2
    myvalues=[math.pow(i/10.0,1.0/gamma) for i in range(10)]

    subplot(subp)
    title(atitle)
    ylabel('Steps')
    xlabel('Location')
    imshow(data,interpolation='nearest',cmap=cm.gray,norm=gammaNorm(gamma=gamma))
    cb=colorbar(spacing='proportional',boundaries=myvalues)
    cb.set_label("probability")


dsubplot("Binary search (deterministic)",d1,211)
dsubplot("Binary search (probabalistic)",d2,212)


savefig("densityplot.svg")
show()


