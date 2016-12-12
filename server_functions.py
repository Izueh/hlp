import time
import datetime
from json import dump, load

hlpdb = 'data/data.json'
writingLock = {}
readingLock = {}


def get_all_groups():
    while hlpdb in writingLock and writingLock[hlpdb]:
        time.sleep(1)
    readingLock[hlpdb] = True
    with open(hlpdb) as f:
        db = load(f)
        groups = db['discussion_groups']

    readingLock.pop(hlpdb)
    return groups


def ag(data):
    data = data.split(' ')
    ugroups = [int(g) for g in data[3].split('\5')]
    response = ''
    groups = get_all_groups()
    for i in range(int(data[1]), int(data[2])):
        if i > len(groups):
            break
        response += '%d. (%s) %s' % \
                    (groups[i]['group_id'], 's' if groups[i]['group_id'] in ugroups else ' ', groups[i]['group_id'])
        response += '\n'
    response.rstrip()
    return response


def p(data):
    query, gID, author, subject, content = data.split('\5')
    groups = get_all_groups()
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
            while hlpdb in writingLock or writingLock[hlpdb] or hlpdb in readingLock or readingLock[hlpdb]:
                time.sleep(1)
            writingLock[hlpdb] = True
            with open(hlpdb, 'w') as f:
                dump({'discussion_groups': groups}, fp=f)
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
    #obtaining all discussion groups
    groups = get_all_groups()
    #formatting response in format:
    #<id>.    <unread posts>   <groups title>
    response = ''
    for i in range(int(data[1]),int(data[2])+int(data[1])):
        if i >= len(groups):
            break
        if groups[i]['group_id'] in ugroups:
            response += '%d. %d %s\n' % \
                    (i,groups[i]['post_count']-read_count[i], groups[i]['title'])
    response.rstrip()
    return response


def rg(data):
    usergroups = data.split('\5')
    ugroups = int(usergroups[3].split('\5'))
    pids = ugroups[1].split('\r\n')
    gid = ugroups[0]
    groups = get_all_groups()
    response = ''

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
                    response += '%d. %s %s %s' % \
                                (post['post_id'], read, post['date'], post['content'])
                    response += '\n'
    response.rstrip()
    return response


def rp(data):
    query, groupid, postid = data.split('\5')
    groups = get_all_groups()
    for g in groups:
        if g['group_id']==groupid:
            for p in g['posts']:
                if p['post_id']==postid:
                    return '\5'.join([p['post_id'],p['subject'],p['author'],p['date'],p['content']])
