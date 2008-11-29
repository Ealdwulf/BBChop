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
