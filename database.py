import threading
import time
import os
from json import dumps, load

hlpdb = 'data/data.json'
writingLock = {}


def get_categories():
    with open(hlpdb) as f:
        return load(f)


def get_group(group):
    with open(hlpdb) as f:
        db = load(f)
        groups = db['discussion_groups']

