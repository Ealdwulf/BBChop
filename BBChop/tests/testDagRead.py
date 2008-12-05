import randomdag
import random
import dagRead


try:
    for test in range(100):
        N=random.randint(10,100)
        dagDef=randomdag.randomdagTxt(N)
        
        dagDefShuffled=dagDef
        random.shuffle(dagDefShuffled)
        
        (dagIds,dagParents)=dagRead.read(dagDefShuffled)
        
        
        dagCheck=dagDef
        for i in range(len(dagDef)):
            dagTerm=dagIds[i]
            for p in dagParents[i]:
                if p>i:
                    raise "invalidDag"
                dagTerm+=' '+dagIds[p]
            if dagTerm not in dagCheck:
                raise "missing term"
            dagCheck=[x for x in dagCheck if x!=dagTerm]
        print "test %d passed" %(test)
except:
    print "FAILED"
    exit(1)

print "PASSED"
exit(0)
