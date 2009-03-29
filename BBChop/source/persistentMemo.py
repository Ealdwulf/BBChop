import os
import os.path
import pickle
import hashlib

#config
pickleProto=pickle.HIGHEST_PROTOCOL
hash=hashlib.sha1

#state
memoObjs=[]
memoDir="/home/ealdwulf/.memoObjs"
if os.path.isdir(memoDir):
    memoObjs=os.listdir(memoDir)
else:
    memoObjs=None

class memo:
    def __init__(self,theClass):
        self.theClass=theClass

    def __call__(self,*args):
        if memoObjs is not None:
            argsStr=pickle.dumps(args,pickleProto)
            hobj=hash()
            hobj.update(argsStr)
            d=hobj.hexdigest()
            fname=os.path.join(memoDir,d)
    
            if d in memoObjs:
                f=open(fname,"rb")
                ret=pickle.load(f)
                f.close()
                return ret
            else:
                ret=self.theClass(*args)
                f=open(fname,"wb")
                pickle.dump(ret,f,pickleProto)
                f.close()
                memoObjs.append(d)
                return ret
        else:
            return self.theClass(*args)
            
        
