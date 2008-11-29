import collStats
from pylab import *
import numpy
import os
import math
import statDb
from analysisRanges import *

namesList=("rate","loc","N","cert","tests","guess","right","lname","lastcountT","lastCountD","seed")
names={}
for i in range(len(namesList)):
    names[namesList[i]]=i

def getStatsOld(fileName):
    f=file(fileName,"r")
    data=[]
    for line in f:
        line=line.replace('(','')
        line=line.replace(')','')
        (rate,loc,N,cert,tests,guess,right,lname,lastCountT,lastCountD,seed)=line.split(',')
        
        data.append([float(rate),int(loc),int(N),float(cert),float(tests),int(guess),right.strip()=='True',lname.strip(),int(lastCountT),int(lastCountD),int(seed)])
    f.close()
    return collStats.collStats(data,names)

def getStats(matchList):
    data=[]
    for (k,v) in statDb.iteritems():

        (rate,loc,N,cert,lastCountT,lastCountD,lname,seed)=k
        (tests,guess,right)=v

        if ((lastCountT,lastCountD),rate) in matchList[1]:
            if N in matchList[0]:
                if cert in matchList[2]:
                    if lname in matchList[4]:
                        data.append([rate,loc,N,cert,tests,guess,right,lname,lastCountT,lastCountD,seed])
    return collStats.collStats(data,names)

def meanEstStd(list):
    return numpy.std(list)/math.sqrt(len(list))


m3=[standardN, rateCountZ,   standardCert,100,lksNames]
m5=[standardN, rateCountV,   standardCert,100,lksNames[:1]]
m6=[steppedN,  rateCountHalf,standardCert,100,lksNames[:1]]
m7=[logN,  rateCountHalf,standardCert,100,lksNames[:1]]

statDb.open()

s3=getStats(m3)
s5=getStats(m5)
s6=getStats(m6)
s7=getStats(m7)

def plots(pfunc,s,atitle,x,y,nonKey,ycomb,legloc,fname,labfn,errcomb=None,axisArgs=None,**kwargs):
    if os.access(fname,os.F_OK):
        print fname,"exists"
    else:
        print "writing ",fname
        g1=s.collate(x,y,nonKey)
        g1c=collStats.collAllStats(g1,ycomb,errcomb)
        
        title(atitle)
        xlabel(x)
        ylabel(y)
        for (key,data) in g1c.iteritems():
            xs=[d[0] for d in data]
            ys=[d[1] for d in data]
            if errcomb is not None:
                yerr=[d[2] for d in data]

                pfunc(xs,ys,yerr=yerr,label=labfn(key),**kwargs)
            else:
                pfunc(xs,ys,label=labfn(key),**kwargs)
            legend(loc=legloc)
        if axisArgs:
            axis(**axisArgs)
        savefig(fname)
        close()



def labfn1(key):
    (cert,lf,lct,lcd)=key
    return "cert=%1.2f %s" %(cert,lf)


plots(plot,s3,atitle="Fault rate vs number of tests",x='rate',y='tests',nonKey=["loc","N","guess","right","seed"],ycomb=numpy.average,legloc=1,fname="plots/faultRate_tests.svg",labfn=labfn1,marker='+')

def countSucc(list):
    return sum(list)/float(len(list))

def labfn2(key):
    (cert,lf,lct,lcd)=key
    
    return "%s lastCount=(%d,%d)" %(lf,lct,lcd)
def labfn3(key):
    (cert,lf)=key
    
    return "cert=%1.2f %s" %(cert,lf)


plots(plot,s3,atitle="Fault rate vs correctness",x='rate',y='right',nonKey=["loc","N","guess","tests","seed"],ycomb=countSucc,legloc=4,fname="plots/faultRate_corr.svg",labfn=labfn1,marker='+')

plots(plot,s5,atitle="Fault rate vs correctness",x='rate',y='right',nonKey=["loc","N","guess","tests","seed","lastcountT","lastCountD"],ycomb=countSucc,legloc=4,fname="plots/faultRate_corr2.svg",labfn=labfn3,marker='+',axisArgs={'ymin':0})
plots(plot,s5,atitle="Fault rate vs number of tests",x='rate',y='tests',nonKey=["loc","N","guess","right","seed","lastcountT","lastCountD"],ycomb=numpy.average,legloc=1,fname="plots/faultRate_tests2.svg",labfn=labfn3,marker='+')

plots(errorbar,s7,atitle="Number of locations vs number of tests, rate=0.5",x="N",y="tests",nonKey=['rate',"loc","guess","seed",'right'],ycomb=numpy.average,errcomb=meanEstStd,legloc=8,fname="plots/N_tests3.svg",labfn=labfn1,marker='+')


ax = subplot(111)
ax.set_xscale('log')

plots(errorbar,s6,atitle="Number of locations vs number of tests, rate=0.5",x="N",y="tests",nonKey=['rate',"loc","guess","seed",'right'],ycomb=numpy.average,errcomb=meanEstStd,legloc=8,fname="plots/N_tests.svg",labfn=labfn1,marker='+')
plots(errorbar,s7,atitle="Number of locations vs number of tests, rate=0.5",x="N",y="tests",nonKey=['rate',"loc","guess","seed",'right'],ycomb=numpy.average,errcomb=meanEstStd,legloc=8,fname="plots/N_tests2.svg",labfn=labfn1,marker='+')

statDb.close()
