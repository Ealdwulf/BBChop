import sys
import randomdag
import dumbdag
import dag
import random

N=30

numTests=100

fail=False



class tester:
    def __init__(self,ref,test):
        self.ref=ref
        self.test=test

    
    def check(self,meth,num,*args):
        res_ref= getattr(self.ref,meth)(*args)
        res_test=getattr(self.test,meth)(*args)

        if res_ref!=res_test:
            print "fail at %d, %s" % (num,meth)
            return True
        else:
            print "passed  %d, %s" % (num,meth)
            return False
        
    

for i in range(10,numTests):
    random.seed(i)
    thisfail=False

    d=randomdag.randomdagDef(N)

    dref=randomdag.randomdag(N,dumbdag,d)
    dtest=randomdag.randomdag(N,dag,d)

    val=[random.randint(0,10) for x in range(N)]

    t=tester(dref,dtest)

    thisfail=t.check("sumUpto",i,val)
    thisfail=t.check("sumAfter",i,val)
    thisfail=t.check("sumOther",i,val)


    fail=fail or thisfail

if fail:
    print "FAILED"
    sys.exit(1)
else:
    print "PASSED"
    sys.exit(0)
    
