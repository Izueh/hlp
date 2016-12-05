import threading
import time
import os
from json import dumps, load
from model import User, create_user, UserDecoder

usersdb = 'data/users/'
hlpdb = 'data/data.json'
writingLock = {}


def register_user(uname):
    fname = usersdb+uname+'.json'
    if fname in os.listdir(usersdb):
        return
    user = User(uname,[])
    while uname in writingLock:
        time.sleep(1)
    writingLock[uname] = 1
    f = open(fname,'w+')

    s = dumps(user, cls=UserDecoder, indent=4)
    f.write(s)
    writingLock.pop(uname)
    f.close()

def get_user(uname):
    fname = usersdb + uname+ '.json'
    with open(fname) as f:
        return load(f, object_hook=create_user)

def get_categories():
    with open(hlpdb) as f:
        return load(f)

def get_posts(group):
    with open(hlpdb) as f:
        db = load(f)
        return db['discussion_groups']