
import numbers
def shannon(probs):
    e=0
    for p in probs:
        if(p>0):
            e-=p*numbers.log(p)
    return e



alpha=numbers.const('1.2')

def renyi(probs):
    e=0
    
    d=1.0/(1.0-alpha)
    for p in probs:
        e=e+numbers.pow(p,alpha)
    return numbers.log(e)*d
