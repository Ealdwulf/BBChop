import numberType
import listUtils

def skipProbsSimple(skipped,dag):

        return [listUtils.cond(s,numberType.one,numberType.zero) for s in skipped]




    
def doGeoDecay(decayFactor,adjacent):
    if len(adjacent)==0:
        return numberType.zero
    decayed = [a*decayFactor for a in adjacent]
    return max(decayed)

def doArithDecay(decayFactor,adjacent):
    if len(adjacent)==0:
        return numberType.zero
    decayed = [a+decayFactor for a in adjacent]
    
    return max(decayed)



class skipProbsDecay:
    def __init__(self,decayFactor,decayFunc):
        self.decayFactor=decayFactor
        self.combFunc = lambda adj: decayFunc(self.decayFactor,adj)

    def __call__(self,skipped,myDag):
        initial = skipProbsSimple(skipped,myDag)

        upto  = myDag.combUpto(initial,self.combFunc)
        after = myDag.combAfter(initial,self.combFunc)
        
        res = [max(initial[i],upto[i],after[i]) for i in xrange(len(skipped))]
        return res
        
