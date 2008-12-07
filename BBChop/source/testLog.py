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

import os

def parseline(line):
    line=line.strip()
    (whereS,detectS)=line.split()
    where=int(whereS)
    if detectS=='True':
        detect=True
    elif detectS=='False':
        detect=False
    elif detectS=='None':
        detect=None
    else:
        raise TypeError
    return(where,detect)
    

class logger:
    
    def __init__(self,logFileName,resume=False):
        self.logFileName=logFileName
        self.resume=resume
        
        if logFileName is not None:
            if resume:
                self.resultsSoFar=[]
                self.logFile=open(logFileName,"r+")
                for line in self.logFile:
                    self.resultsSoFar.append(parseline(line))
                self.logFile.seek(0,os.SEEK_END)
                    
            else:
                self.logFile=open(logFileName,"w")
            self.logging=True
        else:
            self.logging=False
        

    def getResults(self):
        if not self.resume:
            raise "getResult called incorrectly"
        else:
            return self.resultsSoFar


    def log(self,where,detect):
        if self.logging:
            self.logFile.write(str(where)+'\t'+repr(detect)+'\n')
            self.logFile.flush()
            os.fsync(self.logFile.fileno())

        
    def close(self):
        if self.logging:
            self.logFile.close()
        
