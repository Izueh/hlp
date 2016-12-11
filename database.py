import threading
import time
import os
from json import dumps, load

hlpdb = 'data/data.json'
writingLock = {}
readingLock = {}



def get_group(group):
    while writingLock[hlpdb]:
        time.sleep(1)
    with open(hlpdb) as f:
        readingLock[hlpdb]= True
        db = load(f)
        groups = db['discussion_groups']

