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
