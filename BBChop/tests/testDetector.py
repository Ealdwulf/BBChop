from listUtils import listOr
# module which provides a stub detector object for testing
# BBchop. location can be either specified or random.


import random

class detect:
    def __init__(self,N,rate,dag,multi,loc=None,debug=False):
        self.N=N
        if loc==None:
            self.loc=random.randint(0,N-1)
        else:
            self.loc=loc
        self.dag=dag
        if rate is None:
            self.rate=random.random()
        else:            
            self.rate=rate
        if multi:
            self.multiRates=[random.random() for i in range(N)]
        else:
            self.multiRates=None
        self.tests=0
        self.locs=[]
        self.debug=debug
        self.multi=multi

        locList=[False for x in range(N)]
        locList[self.loc]=True

        self.detectable=listOr(dag.anyUpto(locList),locList)



    def test(self,where):
        self.locs.append(where)
        self.tests+=1
        if(self.detectable[where]):
            r=random.random();
            if self.multi:
                ret= (r<self.multiRates[where])
            else:
                ret= (r<self.rate)
        else:
            ret= False
        if self.debug:
            print where,self.loc,ret
        return ret
            

    def printLocs(self):
        for l in self.locs:
            print l,
        print 


    def statusCallback(self,ended,mostLikely,mostLikelyProb,probs,counts):
        if self.debug:
            print ended,mostLikely,mostLikelyProb


