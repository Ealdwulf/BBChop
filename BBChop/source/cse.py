# class for calculating a large number of expressions, repeatedly,
# which contain many common sub expressions.

# The ground values are assumed to be in an array.
# Only  one operator is supported, but it may be varied between calls.
# The operator is assumed to be associative and reflexive.

# all the expressions are calculated in one go, resulting in an array
# containing all the results, mixed in with temporaries.
# when setting up the list of expressions to process, an object is 
# returned which extracts the desired expressions in the original order.

# expressions are identified by their prospective 
# position in the list of temporaries. Ground values are at the start of the 
# list




import copy
from collections import deque

class CommonSubExpressions:

    # constructor. numVals = number of ground values
    def __init__(self,numVals):
        self.numVals=numVals
        self.subExps=[None]*numVals
        self.soFar={}


    # Do not call this, call doCalc on the expListCalc object
    # returned by getExpList

    # calculate all the expressions, using the given 
    # operator (comb), nil term, and ground values.
    # The result is a list of temporaries, some of which are the 
    # required results. 
    def doCalc(self,values,comb,nil):
        if len(values)!=self.numVals:
            raise "initialised woth incorrect value length"

        temp=copy.copy(values)

        for i in range(self.numVals,len(self.subExps)):
            if self.subExps[i] is None:
                temp.append(values[i])
            elif self.subExps[i] is -1:
                temp.append(nil)
            else:
                (a,b)=self.subExps[i]
                temp.append(comb([temp[a],temp[b]]))
        return temp


    # internal function to add a binary expression to the list of 
    # things to calculate. 
    
    def getBinaryExp(self,a,b):
        x=[a,b]
        x.sort()
        x=tuple(x)
        return self.findExp(x)

    # internal - find a binary expression, or add it to the list
    def findExp(self,x):
        if x in self.soFar:
            return self.soFar[x]
        else:
            ret=len(self.subExps)
            self.subExps.append(x)
            self.soFar[x]=ret
            return ret

    # internal return the index of the nil expression
    def getNil(self):
        return self.findExp(-1)

    # Add an expression maybe comprising more or less than 2 ground values
    # l is a list of the ground terms, the expression is assumed to be 
    # l[0] op l[1] op l[2]...


    # In order to promote the chance of subexpression matches, we
    # make the list into an (unbalanced) binary tree
    # which can be thought of as the balanced tree
    # of all ground values, with entries not in l deleted in a breadth-first
    # way.

    # We do this by decorating the list with a temporary copy of 
    # the expression location. This decorated value is refered to
    # as the 'virtual'. We proceed by replacing pairs of terms 
    # whose virtuals are adjacent and whose lower virtual is even.
    # When there are none of these left, the virtuals are divided by two.
    # the exersise repeats until there is only one term left in the list.

    def getExp(self,l):
        if len(l)==0:
            return self.getNil()


        virt=0
        loc=1

        nl=deque([(i,i) for i in l])

        while len(nl)>1:
            next=deque([])
            while len(nl)>1:
                a=nl[0]
                b=nl[1]
                if  (a[virt]+1) == b[virt] and not (a[virt]&1):
                    next.append((a[virt]/2,self.getBinaryExp(a[loc],b[loc])))
                    nl.popleft()
                    nl.popleft()
                else:
                    next.append((a[virt]/2,a[loc]))
                    nl.popleft()
            while len(nl)>0:
                a=nl[0]
                next.append((a[virt]/2,a[loc]))
                nl.popleft()
                
                                
            nl=next
        return nl[0][loc]



    # given a list of expressions, return an object which can calculate them

    def getExpList(self,expList):
        return expListCalc([ self.getExp(toSortedList(expList[i])) for i in range(len(expList))],self)


# This object holds the locations of the wanted expressions in the temporary
# list. It presents a simpler API to the caller than the cse object.
# It is returned by cse.getExpList()

class expListCalc:
    def __init__(self,expList,cse):
        self.expList=expList
        self.cse=cse

    # calculate all the expressions, using the given 
    # operator (comb), nil term, and ground values.
    # We do this by calling cse.doCalc, then extracting the
    # desired expressions from the list of temporaries

    def doCalc(self,values,comb,nil):
        temp=self.cse.doCalc(values,comb,nil)
        res = [temp[self.expList[i]] for i in range(len(self.expList))]
        return res
        

# to increase the commonality, this function is used to 
# sort the ground terms of all expressions we calculate.
# the original argument may be a set, hence the need to 
# convert to a list first.

def toSortedList(x):
    x=list(x)
    x.sort()
    return x
