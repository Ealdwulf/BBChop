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

from BBChop import evidence
import time
import random
from BBChop import likelihoods
from tests import testCases


random.seed(1)

n = 122  # Passes with 121.
d=testCases.testDag(n,False)

i = 0
(counts,locPrior)=testCases.randomEntropyData(i+1,n,d,False,True,10)
# likelihoods.singleRateCalc.probs(counts, locPrior, d)

(ls, lsTot, junk, ls_log) =  likelihoods.singleRate(counts, locPrior, d)
print(ls)
print(lsTot)
print(ls_log)

# assert(lsTot > 0)

likelihoods.probs(counts, locPrior, likelihoods.singleRate ,d)


print(n)
