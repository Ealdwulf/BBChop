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

import evidence
import time
import random
import likelihoods
from tests import testCases


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
