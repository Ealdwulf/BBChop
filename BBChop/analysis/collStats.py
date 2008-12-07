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


import copy


def lind(a):
    return a[0]


class collStats:
    def __init__(self,data,names):
        self.data=data
        self.names=names

    def collate(self,x,y,nonKey):
        collated={}
        for datum in self.data:
            key=copy.copy(datum)
            
            nonKeyList=[x,y]+nonKey
            nonKeyInd=[(self.names[i],i) for i in nonKeyList]
            nonKeyInd.sort(key=lind)

            for (ind,name) in reversed(nonKeyInd):
                del key[ind]

            xi=self.names[x]
            yi=self.names[y]

            key=tuple(key)
            if not collated.has_key(key):
                collated[key]=[]

            term={'x':datum[xi],'y':datum[yi]}
            collated[key].append(term)
        return collated
                
def combYs(terms,comb,errcomb=None):
    xind={}

    for term in terms:
        x=term['x']
        y=term['y']
        if not xind.has_key(x):
            xind[x]=[]
        xind[x].append(y)
        

    xlist=[]
    for (x,ys) in xind.iteritems():
        if errcomb is not None:
            xlist.append((x,comb(ys),errcomb(ys)))
        else:
            xlist.append((x,comb(ys)))

    xlist.sort(key=lind)
    return xlist

            
def collAllStats(stats,comb,errcomb=None):
    res={}
    for (k,terms) in stats.iteritems():
        c=combYs(terms,comb,errcomb)
        res[k]=c
    return res
                
