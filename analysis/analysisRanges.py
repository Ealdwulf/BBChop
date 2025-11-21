#    Copyright 2008 Ealdwulf Wuffinga

#    This file is part of BBChop.
#
#    BBChop is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    BBChop is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with BBChop.  If not, see <http://www.gnu.org/licenses/>.


from BBChop import likelihoods
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


