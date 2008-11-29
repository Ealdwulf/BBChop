import evidence
import time
import random
import likelihoods
import testCases


random.seed(1)



mult=100

out=file("data/N_T.singleRate.csv","w")
for n in range(50,1000,50):





    d=testCases.testDag(n,False)


    for i in range(mult):
        (counts,locPrior)=testCases.randomEntropyData(i+1,n,d,False,True,10)
        start=time.clock()
        junk=evidence.entropiesFast(counts,locPrior,likelihoods.singleRateCalc,d)
        end=time.clock()
        out.write("%d,%f\n" % (n,(end-start)))
    print n

out.close()
                  

