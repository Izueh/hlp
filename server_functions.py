import time
from json import dumps, load

hlpdb = 'data/data.json'
writingLock = {}
readingLock= {}

def get_group():
    while writingLock[hlpdb]:
        time.sleep(1)
    with open(hlpdb) as f:
        db = load(f)
        readingLock[hlpdb] = True
        groups = db['discussion_groups']

    readingLock.pop(hlpdb)
    return groups


def ag(usergroups):
    usergroups= usergroups.split(' ')
    ugroups = [int(g) for g in usergroups[2].split('\5')]

    groups = get_group()
    data = '\n'.join('%d. (%s) %s ' % (g['group_id'],'s' if g['group_id'] in ugroups else ' ' , g['title'] ) for g in groups)

    return data
