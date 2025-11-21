from random import random, seed
#from functools import lru_cache  # TODO works only in python 3.

from BBChop.BBChop import BBChop
from BBChop import likelihoods, dag

class Runner:
    def __init__(self, first_failure_location, failure_rate):
        self.fail_loc = first_failure_location
        self.trials = 0
        self.p = failure_rate
        
        
    def test(self, where):
        ''' Test at given location. '''
        self.trials += 1
        if where >= self.fail_loc:
            return self.p > random()
        else:
            return False
      

    def switch(self, where):
        ''' Switch test location '''
        pass
    def statusCallback(self, ended, mostLikely, mostLikelyProbs, probs, counts):
        '''
        ended: True if testing is done.
        mostLikely: most likely location
        mostLikelyProbs: probability at most likely location
        '''
        #print("Status [{}, {}, {}]".format(ended, mostLikely, mostLikelyProbs))
        pass



#@lru_cache(maxsize=32)
def run_experiment(N, certainty, fail_loc, fail_prob, _seed):
    ''' Runs experiment and returns tuples of facts.
    Those are (loc_found, loc_correct, num_trials)
    '''
    seed(_seed)
    prior = [ 1. / float(N) for i in range(N)]
    runner = Runner(fail_loc, fail_prob)

    finder = BBChop(prior, certainty, runner,
                    likelihoods.singleRateCalc,
                    dag.listDag())

    where = finder.search()
    return (where, fail_loc == where, runner.trials)

def generate_plot(n):
    ''' Generate plot '''
    assert(n == 1)
    N = 100
    certainty = 0.9
    fail_loc = int(N * 0.7)

    data = []
    for fail_prob in [1., .9, .5, .25, .1, 0.05, 0.01   ]:
        print('Running at p={}'.format(fail_prob))
        (where, success, trials) = run_experiment(N, certainty, fail_loc, fail_prob, 1)
        if not success:
            print('Failed with {}'.format(fail_prob))
        data.append((fail_prob, trials))


    import numpy as np
    import matplotlib.pyplot as plt

    probs, trials = zip(*data)
    plt.plot(probs, trials)
    plt.title('semilogx')
    plt.grid(True)
    plt.show()


    #print('Found at {where} ({true}) after {trials} trials.'.format(
           #where=where, true=fail_loc, trials=trials))

if __name__ == '__main__':
    seed(1)
    generate_plot(1)
