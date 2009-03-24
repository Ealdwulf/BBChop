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
        
    

for i in range(numTests):
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
    
