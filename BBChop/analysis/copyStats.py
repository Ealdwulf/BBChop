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



