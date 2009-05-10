import dag
import dagRead
import time
import likelihoods
from BBChop import BBChop
import cProfile


class Cont(Exception):
    pass

class fakeTest:
    def test(self,where):
        raise Cont

    def switch(self,where):
        pass

    def statusCallback(self,ended,mostLikely,mostLikelyProb,probs,counts):
        pass

def runFinder(finder):
    try:
        finder.search()
    except Cont:
        pass




class timer:
    def __init__(self,filename):
        self.log=open(filename,"w")
        self.times=[]

    def run(self,fn,args):
        s=time.time()
        res=fn(*args)
        timeDelta=time.time()-s
        self.times.append(str(timeDelta))
        return res

    def startSet(self,heading):
        self.heading=heading

    def write(self,sep):
        out=self.heading + sep+sep.join(self.times)+"\n"
        self.log.write(out)
    
    def close(self):
        self.log.close()

class profiler:
    def __init__(self,filename):
        self.filename=filename
        self.count=0

    def startSet(self,heading):
        self.heading=heading


    def store(self,res):
        self.res=res

    def run(self,fn,args):

        fname=self.filename+'_'+self.heading+'_'+str(self.count)+'.profile'
        cProfile.runctx('self.store(fn(*args))',globals(),locals(),fname)
        self.count+=1
        return self.res

    def write(self,sep):
        pass

    def close(self):
        pass


runner=profiler("profiles/master")
runner=timer("tlog-master-4b")

for i in [1]: #range(1,10):
    fname="rc"+str(i)+".anc"

    f=file(fname,"r")
    (identifiers,parents)=dagRead.read(f)
    locations=len(identifiers)
    prior=[ 1/float(locations) for i in range(locations)]
    f.close()
    

    runner.startSet(str(i))
    
    thisDag=runner.run(dag.dag,(parents,len(parents)))

    
    finder=BBChop(prior,0.9,fakeTest(),likelihoods.singleRateCalc,thisDag)


    runner.run(runFinder,[finder])
    
    runner.write(" ")
    


runner.close()
    
