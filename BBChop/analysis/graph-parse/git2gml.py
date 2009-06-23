import sys

hasTstamp=True

hash2Id = {}
nodes={}
nodeList=[]

fname=sys.argv[1]

file=open(fname,"r")

import pdb
for line in file:
    tokens=line.split()
    
    if hasTstamp:
        tstamp=tokens.pop(0)

    curr=tokens.pop(0)
    
    parents=tokens

    nodes[curr]={'parents':parents,'children':[]}
    nodeList.append(curr)

# add child links

for node in nodes:
    for parent in nodes[node]['parents']:
        if parent in nodes:
            nodes[parent]['children'].append(node)



# delete broken links
for node in nodes:

    nodes[node]['parents'] = [p for p in nodes[node]['parents'] if p in nodes]
    nodes[node]['children'] = [p for p in nodes[node]['children'] if p in nodes]




# find heads and tails
heads=[]
tails=[]
for node in nodes:
    if len(nodes[node]['children'])==0:
        heads.append(node)
    if len(nodes[node]['parents'])==0:
        tails.append(node)

# add  virtual links to make this a biconnected graph:

nodes['heads']={}
nodes['tails']={}
nodes['heads']['parents']=[]
nodes['heads']['children']=['tails']
nodes['tails']['parents']=['heads']
nodes['tails']['children']=[]

for head in heads:
    nodes[head]['children']='heads'
    nodes['heads']['parents'].append(head)

for tail in tails:
    nodes[tail]['children']='tails'
    nodes['tails']['parents'].append(tail)

nodeList.insert(0,'tails')
nodeList.insert(0,'heads')

# number in reverse, because ogdf doesn't like targets number less than
# sources in directed graphs
maxId=len(nodeList)

for i in xrange(len(nodeList)):
    hash2Id[nodeList[i]]=maxId-i


print """
graph [
    directed 0
"""

for hash in nodeList:
    
    print "node ["
    print "id ",hash2Id[hash]
    print 'label "',hash,'"'
    print ']'
    
    for p in nodes[hash]['parents']:
        if p in hash2Id:
            print "edge ["
            print "source ",hash2Id[hash]
            print "target ",hash2Id[p]
            print "]"

print "]"

