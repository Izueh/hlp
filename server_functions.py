import time
import datetime
from json import dump, load

from collections import OrderedDict

hlpdb = 'data/data.json'
writingLock = {}
readingLock = {}


def get_group():
    while hlpdb in writingLock and writingLock[hlpdb]:
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
    query, gID, author, subject, content = data.split('\5')
    groups = get_group()
    for i in range(len(groups)):
        if groups[i]['group_id'] == gID:
            groups[i]['post_count'] += 1
            groups[i]['posts'].append({
                'post_id': groups[i]['post_count'],
                'subject': subject,
                'author': author,
                'date': datetime.datetime.now().strftime('%b %d %X'),
                'content': content
            })
            while writingLock[hlpdb]:
                time.sleep(1)
            writingLock[hlpdb] = True
            with open(hlpdb, 'w') as f:
                dump({'discussion_groups': groups}, fp=f)
            writingLock.pop(hlpdb)
            return groups[i]


def sg(usergroups):
    usergroups = usergroups.split(' ')
    ugroups = [int(g) for g in usergroups[3].split('\5')]
    data = ''
    groups = get_group()
    for i in range(int(usergroups[1]), int(usergroups[2])):
        if i > len(groups):
            break
        if groups[i]['group_id'] in ugroups:
            data += '%d. (%s) %s' % \
                    (groups[i]['group_id'], 's' if groups[i]['group_id'] in ugroups else ' ', groups[i]['group_id'])
            data += '\n'
    data.rstrip()
    return data


def rg(usergroup):
    usergroups = usergroup.split('\5')
    ugroups = int(usergroups[3].split('\5'))
    pids = ugroups[1].split('\r\n')
    gid = ugroups[0]
    groups = get_group()
    data = ''

    for g in groups:
        if g['group_id'] == gid:
            list = sorted(g['posts'], key=lambda k: k['post_id'], reverse=True)
            x = []
            for l in list:
                if not l['post_id'] in pids:
                    x.append(l)
                    list.remove(l)
            for l in list:
                x.append(l)
            for i in range(int(usergroups[1]), int(usergroups[2])):
                if i < len(x):
                    post = x[i]
                    read = ' '
                    if x[i]['post_id'] in pids:
                        read = 'N'
                    data += '%d. %s %s %s' % \
                            (post['post_id'], read, post['date'], post['content'])
                    data += '\n'
    data.rstrip()
    return data
