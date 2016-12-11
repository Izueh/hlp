import time
import datetime
from json import dump, load

hlpdb = 'data/data.json'
writingLock = {}
readingLock = {}


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
    usergroups = usergroups.split(' ')
    ugroups = [int(g) for g in usergroups[3].split('\5')]
    data = ''
    groups = get_group()
    for i in range(int(usergroups[1]), int(usergroups[2])):
        if i > len(groups):
            break
        data += '%d. (%s) %s' % \
                (groups[i]['group_id'], 's' if groups[i]['group_id'] in ugroups else ' ', groups[i]['group_id'])
        data += '\n'
    data.rstrip()
    return data


def p(data):
    query,gID,author, subject, content = data.split('\5')
    groups = get_group()
    for i in range(len(groups)):
        if groups[i]['group_id'] == gID:
            groups[i]['post_count'] += 1
            groups[i]['posts'].append({
                'post_id': groups[i]['post_count'],
                'subject': subject,
                'author': author,
                'date': datetime.datetime.now(),
                'content': content
            })
            while writingLock[hlpdb]:
                time.sleep(1)
            writingLock[hlpdb] = True
            with open(hlpdb,'w') as f:
                dump({'discussion_groups':groups},fp=f)
            writingLock.pop(hlpdb)
            return groups[i]



def sg(usergroups):
    usergroups= usergroups.split(' ')
    ugroups = [int(g) for g in usergroups[3].split('\5')]
    data = ''
    groups = get_group()
    for i in range(int(usergroups[1]),int(usergroups[2])):
        if i > len(groups):
            break
        if groups[i]['group_id'] in ugroups:
            data += '%d. (%s) %s' % \
                    (groups[i]['group_id'],'s' if groups[i]['group_id'] in ugroups else ' ', groups[i]['group_id'])
            data +='\n'
    data.rstrip()
    return data