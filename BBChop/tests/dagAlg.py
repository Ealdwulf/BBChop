import copy
def childLists2Rel(childLists):
        childRel={}
        for n in range(len(childLists)):
            for c in childLists[n]:
                childRel[(n,c)]=1
        return childRel

#Warshall's algorithm
def transitiveClosure(rel,N):
    closedRel=copy.copy(rel)
    for j in range(N):
        for i in range(N):
            if closedRel.has_key((i,j)):
                for k in range(N):
                    if closedRel.has_key((j,k)):
                        closedRel[(i,k)]=1
    return closedRel
