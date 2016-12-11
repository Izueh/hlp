import threading
import time
import os
from json import dumps, load

hlpdb = 'data/data.json'
writingLock = {}
readingLock= {}

def get_group(group):
    while writingLock[hlpdb]
        time.sleep(1)

    with open(hlpdb) as f:
        db = load(f)
        readingLock[hlpdb] = True
        groups = db['discussion_groups']

    readingLock.pop(hlpdb)
