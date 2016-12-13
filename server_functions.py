import time
import datetime
from json import dump, load

hlpdb = 'data/data.json'
writingLock = {}
readingLock = {}

# internal method used to obtain information on ALL discussion
# groups in server
# @return list of all discussion groups as dictionaries
def get_all_groups():
    while hlpdb in writingLock and writingLock[hlpdb]:
        time.sleep(1)
    readingLock[hlpdb] = True
    with open(hlpdb) as f:
        db = load(f)
        groups = db['discussion_groups']

    readingLock.pop(hlpdb)
    return groups

# server-side 'all groups'. Parses client side 'ag' request 
# and formats response for client
# @param data raw input given from client to server
# @return formatted string to reply to client
def ag(data):
    data = data.split(' ')
    ugroups = [int(g) for g in data[3].split('\5')] if data[3] is not '' else []
    response = ''
    groups = get_all_groups()
    for i in range(int(data[1]), int(data[2])+int(data[1])):
        if i >= len(groups):
            break
        response += '%d. (%s) %s' % \
                    (groups[i]['group_id'], 's' if groups[i]['group_id'] in ugroups else ' ', groups[i]['title'])
        response += '\n'
    response.rstrip()
    return response


# server-side 'p'. Parses client side 'p' request 
# and formats response for client
# @param data raw input given from client to server
# @return formatted string to reply to client 
def p(data):
    gID, author, subject, content = data[2:].split('\5')
    gID=int(gID)
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
            while hlpdb in writingLock or hlpdb in readingLock:
                time.sleep(1)
            writingLock[hlpdb] = True
            with open(hlpdb, 'w') as f:
                dump({'discussion_groups': groups}, fp=f)
            writingLock.pop(hlpdb)
            return groups[i]

# server-side 'subscribed groups'. Parses client side 'sg' request 
# and formats response for client
# @param data raw input given from client to server
# @return formatted string to reply to client
def sg(data):
    #input does not only contain usergroups
    #of the form: 'sg 4 7 1\x0520\x052\x0510'
    data = data.split(' ')
    groups_read_count = [int(g) for g in data[3].split('\5')] if data[3] is not '' else []

    # groups_read_count = data[3].split('\5')
    ugroups = [] #ids of subscribed groups
    read_count = [] #count of posts read
    for x in range(0, len(groups_read_count)-1, 2):
        #populating above
        ugroups.append(groups_read_count[x])
        read_count.append(groups_read_count[x+1])
    #obtaining all discussion groups
    groups = get_all_groups()
    #formatting response in format:
    #<id>.    <unread posts>   <groups title>
    response = ''
    for i in range(int(data[2]),int(data[2])+int(data[1])):
        if i >= len(groups):
            break
        if groups[i]['group_id'] in ugroups:
            index = ugroups.index(groups[i]['group_id']) # EDGAR: we can't use I for read_count we have to find the index of
            # the group in ugroups not in groups this should fix it
            response += '%d. %d %s\n' % \
                    (i,groups[i]['post_count']-read_count[index], groups[i]['title'])
    response.rstrip()
    return response if response != "" else "Not subscribed to any groups"

# server-side 'read group'. Parses client side 'rg' request 
# and formats response for client
# @param data raw input given from client to server
# @return formatted string to reply to client
def rg(data):
    usergroups = data.split('\5')
    query,start,end = usergroups[0].split(' ')
    start = int(start)
    end = int(end)+1

    #format of usergroups for no read posts in group with id of 1
    #['rg 10 0 ', '1', '']
    ugroups = int(usergroups[1].split('\5'))
    pids = ugroups[2].split('\r\n') if ugroups[2] is not '' else []
    gid = ugroups[1]
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
            for i in range(start, end):
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

# server-side 'rp'. Parses client side 'rp' request 
# and formats response for client
# @param data raw input given from client to server
# @return formatted string to reply to client
def rp(data):
    query, groupid, postid = data.split('\5')
    groups = get_all_groups()
    for g in groups:
        if g['group_id']==groupid:
            for p in g['posts']:
                if p['post_id']==postid:
                    return '\5'.join([p['post_id'],p['subject'],p['author'],p['date'],p['content']])
