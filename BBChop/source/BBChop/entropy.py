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

import numberType
def shannon(probs):
    e=0
    for p in probs:
        if(p>0):
            e-=p*numberType.log(p)
    return e



alpha=numberType.const('1.2')

def renyi(probs):
    e=0
    one=numberType.const(1.0)
    d=one/(one-alpha)
    for p in probs:
        e=e+numberType.pow(p,alpha)
    return numberType.log(e)*d
