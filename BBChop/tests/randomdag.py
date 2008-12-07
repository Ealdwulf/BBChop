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
import random
import dag
import copy
import dagAlg

#return a random connected dag with unique top and bottom

tailWeight=0.2
branchWeight=0.6

def sortDec(d,i,j):
    if d.has_key((i,j)):
        return -1
    elif d.has_key((j,i)):
        return 1
    else:
        return 0
    

class rdag:
    def __init__(self):
        self.nodes=[[]] # each node is a list of the indexes of its children
        self.bottomNodeIndex=0

    def randomLoc(self,exclude):
        where=self.bottomNodeIndex
        while where in exclude:
            where=random.randint(0,len(self.nodes)-1)
        return where


    def addTail(self):
        newNode=[]
        self.nodes.append(newNode)
        self.nodes[self.bottomNodeIndex].append(len(self.nodes)-1)
        self.bottomNodeIndex=len(self.nodes)-1
        

    def addBefore(self,where):
        oldNode=self.nodes[where]
        newNode=[len(self.nodes)]
        self.nodes.append(oldNode)
        self.nodes[where]=newNode
        return len(self.nodes)-1

    def movechild(self,fromNode,toNode,childNum):
        childInd=self.nodes[fromNode][childNum]
        self.nodes[toNode].append(childInd)
        del self.nodes[fromNode][childNum]


    def addBranch(self,where):
        newNode=copy.copy(self.nodes[where])
        self.nodes.append(newNode)
        for n in self.nodes:
            if where in n:
                n.append(len(self.nodes)-1)

    def addRandom(self):
        x=random.random()
        if x<tailWeight or len(self.nodes)<=2:
            self.addTail()
        elif x<branchWeight:
            self.addBranch(self.randomLoc([0,self.bottomNodeIndex]))
        else:
            one=self.randomLoc([self.bottomNodeIndex])
            two=self.addBefore(one)
            self.randomMoveChildren(one,two)

    def randomMoveChildren(self,one,two):
            select=[random.randint(0,1) for i in self.nodes[two]]
            if sum(select)==0:
                select[random.randint(0,len(select)-1)]=1
            for i in reversed(range(len(select))):
                if not select[i]:
                    self.movechild(two,one,i)
        

    def sort(self):

        index=[]
        rest=range(len(self.nodes))


        # dumb selection sort
        while len(rest)>0:
            for i in range(len(rest)):
                if all([c in index for c in self.nodes[rest[i]]]):
                    index.insert(0,rest[i])
                    del rest[i]
                    break



        rindex=[0 for i in index]
        for i in range(len(index)):
            rindex[index[i]]=i

        newdag=[[rindex[j] for j in self.nodes[i]] for i in index]
        self.nodes=newdag

    
            
def printRel(r,N):
    for i in range(N):
        for j in range(N):
            if r.has_key((i,j)):
                print "1",
            else: 
                print "0",
        print 

               


def randomdagDef(N):
    rd=rdag()
    for i in range(1,N):
        rd.addRandom()

    rd.sort()

    
    parents=[[] for i in range(N)]
    

    for i in range(N):
        for c in rd.nodes[i]:
            parents[c].append(i)

    return parents


       
def randomdagTxt(N,parents=None):
    if parents is None:
        parents=randomdagDef(N)
    
    di=[' '.join(map(str,[i]+parents[i])) for i in range(len(parents))]
    return di

def randomdag(N,dagModule=dag,parents=None):
    if parents is None:
        parents=randomdagDef(N)

    d=dagModule.dag(parents,N)

    return d
         

    
        
if __name__=='__main__':
    random.seed(1)
    r=randomdag(10)
    
    print r
