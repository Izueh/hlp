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

def sg(data):
    #input does not only contain usergroups
    #of the form: 'sg 4 7 1\x0520\x052\x0510'
    data = data.split(' ')
    groups_read_count = data[3].split('\5')
    ugroups = [] #ids of subscribed groups
    read_count = [] #count of posts read
    for x in range(0, len(groups_read_count)-1, 2):
        #populating above
        ugroups.append(int(groups_read_count[x]))
        read_count.append(int(groups_read_count[x+1]))

    response = ''
    #obtaining all discussion groups
    groups = get_group()
    #formatting response in format:
    #<id>.    <unread posts>   <groups title>
    for i in range(int(data[1]),int(data[2])+int(data[1])):
        if i >= len(groups):
            break
        if groups[i]['group_id'] in ugroups:
            response += '%d. %d %s\n' % \
                    (i,groups[i]['post_count']-read_count[i], groups[i]['title'])
    response.rstrip()
    return response

def rg(usergroup):
    usergroups = usergroups.split(' ')
    ugroups = int(usergroups[3].split('\5'))
    pids = ugroups[1].split('\r\n')
    gid = ugroups[0]
    groups = get_group()
    data = ''
    for g in groups:
        if g['group_id'] == gid:
            for i in range (int(usergroups[1]), int(usergroups[2])):
                post = g['posts'][i]
                read = ' '
                if post['post_id'] in pids:
                    read = 'N'
                data += '%d.%s%s %s %s %s %s' % \
                        (post['post_id'], read, post['month'], post['day'], post['time'], post['content'])
                data += '\n'
    data.rstrip()
    return data
