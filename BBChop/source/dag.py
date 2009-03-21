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


from listUtils import listSub,prod,listComb,listCond
# class for computing over directed acyclic graphs.
# values are held outside the graph object, in lists


# the dag is defined by a parents relation: for each index, which indexes are its parents.

# NB the following is true, but proved less useful than I hoped, so could be removed:
# it is required that < and > on indexes is consistent with the transitive closure of the parents
# relation. That is, if parent*(a,b) then a<b and b>a. This is checked.


class IllFormedDAGFile(Exception): pass

class DAGWrongLength(Exception): pass

def union(args):
    res=set()
    for a in args:
        res=res.union(a)
    return res
    

# abstract dag class: defines sum,and type functions in terms of comb functions
class absDag:
    def sumUpto(self,values):
        return self.combUptoSingle(values,sum)
    
    def sumAfter(self,values):
        return self.combAfterSingle(values,sum)
        
    def anyUpto(self,values):
        return self.combUpto(values,any)
    
    def anyAfter(self,values):
        return self.combAfter(values,any)

    def anyOther(self,values):        
        so=self.sumOther(values)
        res=[s>0 for s in so]
        return res

    def prodAfter(self,values):
        return self.combAfterSingle(values,prod)
    
    def unionUpto(self,values):
        return self.combUpto(values,union)
        
    def unionAfter(self,values):
        return self.combAfter(values,union)
        
   

class dag(absDag):
    def __init__(self,parents,N):

        self.parents=parents
        
        children=[[] for i in range(N)]
        

        for i in range(N):
            for p in parents[i]:
                children[p].append(i)

        self.children=children
            
        # a linear stretch ends if a node has multiple children or its child has multiple parents
        self.linearEnd=  [len(children[i])!=1 or len(parents[children[i][0]])!=1 for i in range(N)] 
        # a linear stretch starts if a node has multiple parents or its parent has multiple children
        self.linearStart=[len(parents[i])!=1 or len(children[parents[i][0]])!=1 for i in range(N)]

        loc=[set([i]) for i in range(N)]
        empty=[set() for i in range(N)]
        locE=listCond(self.linearEnd,loc,empty)
        locS=listCond(self.linearStart,loc,empty)
        
        self.multiUpto=self.unionUpto(locE)
        self.multiUpto=listCond(self.linearStart,self.multiUpto,empty)
        
        self.multiAfter=self.unionAfter(locS)
        self.multiAfter=listCond(self.linearEnd,self.multiAfter,empty)
        

    def getParents(self,loc):
        return self.parents[loc]


    def combUptoSingle(self,values,comb):

        linear=self.combUptoLinear(values,comb)
        linearS=listComb(comb,linear,values)
        multi=self.combUptoMulti(linearS,comb)
        linear2=self.combUptoLinear(multi,comb)
        res=listComb(comb,linear,linear2,multi)
        return res

    def combAfterSingle(self,values,comb):

        linear=self.combAfterLinear(values,comb)
        linearS=listComb(comb,linear,values)
        multi=self.combAfterMulti(linearS,comb)
        linear2=self.combAfterLinear(multi,comb)
        res=listComb(comb,linear,linear2,multi)
        return res

    def combUptoLinear(self,values,comb):
        res=[comb([])]*len(values)

        for i in range(len(values)):
            if not self.linearStart[i]:
                res[i]=comb([comb([values[j],res[j]]) for j in self.parents[i]])
        return res


    def combAfterLinear(self,values,comb):
        res=[comb([])]*len(values)

        for i in reversed(range(len(values))):
            if not self.linearEnd[i]:
                res[i]=comb([comb([values[j],res[j]]) for j in self.children[i]])
        return res


    def combUptoMulti(self,linear,comb):
        res=[comb([])]*len(linear)
        
        for i in range(len(linear)):
            res[i]=comb([linear[j] for j in self.multiUpto[i]] )
        return res

    def combAfterMulti(self,linear,comb):
        res=[comb([])]*len(linear)
        
        for i in reversed(range(len(linear))):
            res[i]=comb([linear[j] for j in self.multiAfter[i]] )
        return res

    # these methods assume the consistentency defined above.

    # for each location, return the sum of lower locations from values
    def combUpto(self,values,comb):
        res=[comb([])]*len(values)

        for i in range(len(values)):
            res[i]=comb([comb([values[j],res[j]]) for j in self.parents[i]])
        return res


    # for each location, return the sum of higher locations from values
    def combAfter(self,values,comb):
        res=[comb([])]*len(values)
        
        for i in reversed(range(len(values))):
            res[i]=comb([comb([values[j],res[j]]) for j in self.children[i]])
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


# like dag, but assumes linear order
class listDag(absDag):

    def getParents(self,loc):
        if loc==0:
            return []
        else:
            return [loc-1]
        

    def combUptoSingle(self,values,comb):
        tot=comb([])
        res=[]
        for v in values:
            res.append(tot)
            tot=comb([tot,v])
        return res

    def combUpto(self,values,comb):
        return self.combUptoSingle(values,comb)

    def combAfterSingle(self,values,comb):
        tot=comb([])
        res=[]
        for v in reversed(values):
            res.append(tot)
            tot=comb([tot,v])
        res.reverse()
        return res

    def combAfter(self,values,comb):
        return self.combAfterSingle(values,comb)

    
    def sumOther(self,values):
        # no others in total order

        return [0] * len(values)





listDagObj=listDag()



def linearTestDag(N):
    parents=['%d %d' %(a+1,a) for a in range(N-1)]
    parents[:0]='0'
    return dag(parents,N)


