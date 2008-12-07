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

import statDb


def mergeStats(fileName):
    f=file(fileName,"r")
    
    for line in f:
        line=line.replace('(','')
        line=line.replace(')','')
        line=line.replace("'",'')
        
        (rate,loc,N,cert,tests,guess,right,lname,lastCountT,lastCountD,seed)=line.split(',')
        

        key=(float(rate),int(loc),int(N),float(cert),int(lastCountT),int(lastCountD),lname.strip(),int(seed))
        result=(float(tests),int(guess),right.strip()=='True')
        statDb.add(key,result)
    f.close()



statDb.create()
mergeStats("data/stats1.csv")
mergeStats("data/stats3.csv")
mergeStats("data/stats5.csv")
mergeStats("data/stats6.csv")
statDb.close()



