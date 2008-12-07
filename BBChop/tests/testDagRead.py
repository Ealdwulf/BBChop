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
import randomdag
import random
import dagRead


try:
    for test in range(100):
        N=random.randint(10,100)
        dagDef=randomdag.randomdagTxt(N)
        
        dagDefShuffled=dagDef
        random.shuffle(dagDefShuffled)
        
        (dagIds,dagParents)=dagRead.read(dagDefShuffled)
        
        
        dagCheck=dagDef
        for i in range(len(dagDef)):
            dagTerm=dagIds[i]
            for p in dagParents[i]:
                if p>i:
                    raise "invalidDag"
                dagTerm+=' '+dagIds[p]
            if dagTerm not in dagCheck:
                raise "missing term"
            dagCheck=[x for x in dagCheck if x!=dagTerm]
        print "test %d passed" %(test)
except:
    print "FAILED"
    exit(1)

print "PASSED"
exit(0)
