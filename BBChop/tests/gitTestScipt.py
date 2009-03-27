#!/usr/bin/python

import testDetector
import dagRead
import os
import dag 
import sys


class doExit(Exception):
     def __init__(self, value):
         self.value = value


isGit = os.environ['TEST_SEARCHER']=='git'
print isGit
try:
    ancestryFilename=os.environ['TEST_ANCESTRY']
    testDir = os.environ["TEST_DIR"]
    loc=int(os.environ['TEST_LOC'])
    
    f=file(ancestryFilename,"r")
    (identifiers,parents)=dagRead.read(f)
    f.close()
    N=len(parents)
    thisDag=dag.dag(parents,N)
    t=testDetector.detect(N,1.0,thisDag,False,loc)
    
    numbers={}
    for i in range(len(identifiers)):
        numbers[identifiers[i]]=i
    
    if isGit:
        os.system("git rev-parse HEAD >$TEST_DIR/__head__")
        where=open(testDir+"/__head__","r").readline().strip()
        where=numbers[where]
    else:
        where = sys.argv[1]
        where=numbers[where]

    os.system("echo 'foo' >>$TEST_DIR/tries")

    
    if t.test(where):
        print "bad"
        raise doExit(1)
    else:
        print "good"
        raise doExit(0)

except doExit, e:
    exit(e.value)
except:
    exit(-1)
