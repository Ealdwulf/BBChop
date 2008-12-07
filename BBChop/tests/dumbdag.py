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
import dagAlg
from listUtils import listSub,prod
# class for computing over directed acyclic graphs.
# values are held outside the graph object, in lists

# the dag is defined by a parents relation: for each index, which indexes are its parents.
# it is required that < and > on indexes is consistent with the transitive closure of the parents
# relation. That is, if parent*(a,b) then a<b and b>a. This is checked.

# this version of the class has a simple O(N^2) implementation for test purposes


class IllFormedDAGFile(Exception): pass

class DAGWrongLength(Exception): pass



# abstract dag class: defines sum,and type functions in terms of comb functions
class absDag:
    def sumUpto(self,values):
        return self.combUpto(values,sum)
    
    def sumAfter(self,values):
        return self.combAfter(values,sum)
        
    def anyUpto(self,values):
        return self.combUpto(values,any)
    
    def anyAfter(self,values):
        return self.combAfter(values,any)

    def prodAfter(self,values):
        return self.combAfter(values,prod)
    

   

class dag(absDag):
    def __init__(self,parents,N):

        self.parents=parents
        
        children=[[] for i in range(N)]
        

        for i in range(N):
            for p in parents[i]:
                children[p].append(i)

        self.children=children
            
        childRel=dagAlg.childLists2Rel(self.children)
        self.decendentRel=dagAlg.transitiveClosure(childRel,N)


    # these methods assume the consistentency defined above.

    # for each location, return the sum of lower locations from values
    def combUpto(self,values,comb):
        res=[comb([v for (i,v) in enumerate(values) if self.decendentRel.has_key((i,j))]) for j in range(len(values))]

        return res


    # for each location, return the sum of higher locations from values
    def combAfter(self,values,comb):
        res=[comb([v for (i,v) in enumerate(values) if self.decendentRel.has_key((j,i))]) for j in range(len(values))]
        return res


    # for each location, return the sum of locations neither lower or higher from values
    # we do this by taking the total and subtracting everything else.
    def sumOther(self,values,sumUpto=None,sumAfter=None):
        # save recalculating sumUpto/After if already known
        if sumUpto is None:
            sumUpto=self.sumUpto(values)

        if sumAfter is None:
            sumAfter=self.sumAfter(values)

        sums=[sum(values)]*len(values)

        # 
        sums=listSub(sums,values,sumUpto,sumAfter)
        return sums




def linearTestDag(N):
    parents=['%d %d' %(a+1,a) for a in range(N-1)]
    parents[:0]='0'
    return dag(parents,N)


