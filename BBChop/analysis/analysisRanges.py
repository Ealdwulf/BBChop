import likelihoods
import math

standardN=[100]
steppedN=range(100,1000,100)
logN = [int(math.pow(10,p/10.0)) for p in range(10,35)]

rateCountZ=[((0,0),r/10.0) for r in range(9,0,-2)]
rateCountV=[((10-r,r),r/10.0) for r in range(9,0,-1)]
rateCountHalf=[((0,0),5/10.0)]

standardCert=[0.7,0.8,0.9]


lks=          [likelihoods.singleRateCalc,likelihoods.multiRateCalc]
lksNames=[l.name() for l in lks]


