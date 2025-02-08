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
            if (i,j) in closedRel:
                for k in range(N):
                    if (j,k) in closedRel:
                        closedRel[(i,k)]=1
    return closedRel
