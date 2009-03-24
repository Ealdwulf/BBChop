import os
import dagRead


gitRepo = "/home/ealdwulf/Progs/git-trees/git"
failVer = "v1.6.2"
passVer = "v1.6.0"
testDir = gitRepo+"/test.delete"


ancFname =  testDir + "/anc.txt"
os.environ['TEST_ANCESTRY'] = ancFname


def sysc(cmd):
    print cmd,"->"
    os.system(cmd)

sysc("mkdir -p "+testDir)
os.environ["TEST_DIR"] = testDir


os.chdir(gitRepo)
os.system("$topdir/interfaces/git/git-bbchop-list "+failVer+" ^"+passVer+" >$TEST_ANCESTRY")
ancFile=open(ancFname,"r")
(identifiers,parents)=dagRead.read(ancFile)
N=len(parents)

gitcmd = "./git "

import pdb
def testGit(rev):
    os.environ['TEST_LOC']=str(rev)
    os.environ['TEST_SEARCHER']="git"
    try:
        sysc("cp /dev/null $TEST_DIR/tries")
        sysc(gitcmd + "bisect start")
        sysc(gitcmd + "bisect bad "+ failVer)
        sysc(gitcmd + "bisect good "+passVer)
        sysc(gitcmd + "bisect run $topdir/tests/gitTestScipt.py |tee $TEST_DIR/bisectLog")

        sysc('grep "is first bad commit" $TEST_DIR/bisectLog >$TEST_DIR/result')
        where=open(testDir+"/result","r").readline().split()[0]
        sysc('wc -l  $TEST_DIR/tries >$TEST_DIR/count')
        count=int(open(testDir+"/count","r").readline().split()[0])
        return (where==identifiers[rev],count)

    finally:
        sysc(gitcmd + "bisect reset")

bbchopcmd = "$topdir/source/bbchop "
def testBBChop(rev):
    os.environ['TEST_LOC']=str(rev)
    os.environ['TEST_SEARCHER']="bbchop"
    try:
        sysc(bbchopcmd + "-a $TEST_ANCESTRY -g $TEST_DIR/bbchop.log -t $topdir/tests/gitTestScipt.py -k deterministic -c 0.999 |tee $TEST_DIR/bisectLog")
        sysc("grep 'Search complete' $TEST_DIR/bisectLog > $TEST_DIR/result")
        where=open(testDir+"/result").readline().split()[6]
        count=int(open(testDir+"/count","r").readline().split()[0])

        return (where==identifiers[rev],count)
        
    finally:
        pass


log=open(testDir + "/log","w")



for i in range(N):
    (gitSucc,gitTries)=testGit(i)
    (bbSucc,bbTries)=testBBChop(i)
    res=(gitSucc,gitTries,bbSucc,bbTries)
    log.write(str(res)+"\n")
    log.flush()

log.close()


