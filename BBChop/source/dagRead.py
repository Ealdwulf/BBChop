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


# read a dag description, returning identifiers and dag structure.

# a dag file has the format:
# nodeId [parentId ]*

# we return a list of identifiers, as strings, topologically sorted so that
# no parent is after a child. This is essential because:
#  - BBChop internally identifies nodes by their node number
#  - The module dag.py assumes that no parent has a node number > than its 
#    child.
# The node number of an identifier is its location in this list, starting 
# from 0. In fact, all data in BBChop is held in lists such that the data 
# corresponding to a node numbered i is at location i in the list.
#
# We also return the node numbers of the parents for each node 
# - in exactly such a list.



import copy

class coll:
    pass


# depth first seach, for topological sort
class dfs:
    def __init__(self,dag):
        self.visited={}
        self.dag=dag
        self.sorted=[]

        for node in self.dag:
            if node not in self.visited:
                s=coll()
                s.node=node
                s.toDo=copy.copy(self.dag[s.node])
                self.visited[s.node]=1
                self.dfsVisit([s])


    def dfsVisit(self,stack):

        while len(stack)>0:
            while len(stack[-1].toDo)>0:
                parent=stack[-1].toDo.pop(0)
                if parent not in self.visited:
                    s=coll()
                    s.node=parent
                    s.toDo=copy.copy(self.dag[s.node])
                    self.visited[s.node]=1                    
                    stack.append(s)
            self.sorted.append(stack[-1].node)
            stack.pop()



def sortDag(dag):
    x=dfs(dag)
    return x.sorted


def read(inputFile):

    dag={}
    
    for line in inputFile:

        lineParts=line.split()

        node=lineParts[0]

        lineParts.pop(0)

        parents=lineParts

        dag[node]=parents

    

    # node ids in sorted order
    identifiers=sortDag(dag)


    # which node id is where
    dagLocs={}
    for i in range(len(identifiers)):
        dagLocs[identifiers[i]]=i

    
    dagStruct=[]
    for id in identifiers:
        parentLocs=[dagLocs[p] for p in dag[id]]
        dagStruct.append(parentLocs)

    return (identifiers,dagStruct)

