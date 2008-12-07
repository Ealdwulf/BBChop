#!/usr/bin/python
# filter the output of git-rev-list,
# for use by BBChop

import sys
import re
parents=[]
ids=[]
for line in sys.stdin:
    
    # chop off any annotation, leaving only what we want
    bra=line.find('(')
    if bra!=-1:
        line=line[:bra]
    idpar=line.split()
    ids.append(idpar[0])
    parents.append(idpar[1:])

# now do the output

for i in range(len(ids)):
    print ids[i]," ",
    thispar=[p for p in parents[i] if p in ids]
    print ' '.join(thispar)
