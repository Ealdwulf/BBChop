import anydbm
import pickle

filename="data/statsdb"

global theDB


def open():
    global theDB
    theDB=anydbm.open(filename,"w")
def create():
    global theDB
    theDB=anydbm.open(filename,"c")



def close():
    theDB.close()

def add(key,value):
    theDB[pickle.dumps(key)]=pickle.dumps(value)

def get(key):
    return pickle.loads(theDB[pickle.dumps(key)])
def has_key(key):
    return theDB.has_key(pickle.dumps(key))

def iteritems():
    global theDB
    for (key,value) in theDB.iteritems():
        yield (pickle.loads(key),pickle.loads(value))
