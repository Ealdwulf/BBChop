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

from pylab import *
import numpy

dataFile=file("data/N_T.singleRate.csv","r")
lines=dataFile.readlines()
dataFile.close()

data=[l.strip().split(',') for l in lines]
data=[(int(d[0]),float(d[1])) for d in data]

coll={}

for (N,time) in data:
    if coll.has_key(N):
        coll[N].append(time)
    else:
        coll[N]=[time]

coll=[v for v in coll.iteritems()]
coll.sort(key=lambda x:x[0])


x=[]
y=[]
yerr=[]

for (N,times) in coll:
    x.append(N)
    y.append(numpy.average(times))
    yerr.append(numpy.std(times))

    
title("Average time taken for entropy calculation")
ylabel('seconds')
xlabel('number of revisions')
plot(x,y,marker='+')
savefig("plots/timeplot.svg")

show()
