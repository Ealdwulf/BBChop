import numberType
import listUtils

def skipProbsSimple(skipped,dag):

        return [listUtils.cond(s,numberType.one,numberType.zero) for s in skipped]




class doGeoDecay:
    def __init__(self,decayFactor):
        self.decayFactor=numberType.pow(decayFactor,numberType.const(0.5))

    def __call__(self,adjacent):
        if len(adjacent)==0:
            return numberType.zero
        decayed = [a*self.decayFactor for a in adjacent]
        return max(decayed)

class doArithDecay:
    def __init__(self,decayFactor):
        self.decayFactor=decayFactor/numberType.const(2)

    def __call__(self,adjacent):
        if len(adjacent)==0:
            return numberType.zero
        decayed = [a+self.decayFactor for a in adjacent]
        
        return max(decayed)



class skipProbsDecay:
    def __init__(self,decayFactor,decayFunc):
        self.decayFactor=decayFactor

        # NB, the dag comb() methods don't really work as a generic 
        # propagation method. They assume their arguments are associative, so in fact the decay
        # factor gets applied twice. The above classes have to work round this.


        self.combFunc = decayFunc(self.decayFactor)

    def __call__(self,skipped,myDag):
        initial = skipProbsSimple(skipped,myDag)



        upto  = myDag.combUpto(initial,self.combFunc)
        after = myDag.combAfter(initial,self.combFunc)
        
        res = [max(initial[i],upto[i],after[i]) for i in xrange(len(skipped))]
        return res
        
