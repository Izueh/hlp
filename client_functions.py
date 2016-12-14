from json import load, dump
from os import listdir

NOT_LOGGED_IN = "Not logged in. Please log in before using the forum.\n"
HELP = '''Usage: COMMAND [ARG]
    login USERID\tDetermines which discussion groups you are to and which posts you have read
    help\tPrints this help menu of supported commands and subcommands
    ag [N] \tList the names of all existing discussion groups optional argument N at a time
    \ts N\tSubscribe to groups by specifying the group number
    \tu N\tUnsubscribe from groups by specifying the group number
    \tn\tList the next N discussion groups. Exits ag command when all N groups displayed
    \tq N\tQuit ag command
    sg [N]\tList the names of all subscribed groups optional argument N at a time
    rg GNAME [N]\tDisplays the status of all posts in group GNAME, optional argument N at a time
    \t[id]\tNumber between 1 and N denoting the post within the list of posts to display
    \t\tn\tDisplays at most N more lines of post content.
    \t\tq\tQuits subcommand [id]
    \tr N [M]\tMarks a post as read. Takes in a number N or range of numbers N - M
    \tn\tLists the next N posts. Exits rg command when all N posts displayed
    \tp\tPost to the group
    \tq\tQuit rg command
    logout\tLogs out current user\n\n\n\n'''

AG_HELP = '''\ts N\tSubscribe to groups by specifying the group number
    \tu N\tUnsubscribe from groups by specifying the group number
    \tn\tList the next N discussion groups. Exits ag command when all N groups displayed
    \tq N\tQuit ag command\n\n\n\n'''

RG_HELP = '''    \t[id]\tNumber between 1 and N denoting the post within the list of posts to display
    \t\tn\tDisplays at most N more lines of post content.
    \t\tq\tQuits subcommand [id]
    \tr N [M]\tMarks a post as read. Takes in a number N or range of numbers N - M
    \tn\tLists the next N posts. Exits rg command when all N posts displayed
    \tp\tPost to the group
    \tq\tQuit rg command'''


# login methods that checks if there's a user 
# file for the current user on this machine
# @param username current user's username
# @param data raw input provided by user
# @return username username of current user
def login(username, data):
    username = data.split(' ')[1]
    check_user(username)
    return username

# checks if there's someone currently logged in
# @param username variable holding name of currently
# logged in user
# @return true if there's a user logged in, false otherwise.
def is_logged_in(username):
    return False if username is None else True

# provides feedback for operations in which user needs to log in
def not_logged_in():
    print(NOT_LOGGED_IN)
    print(HELP)

# checks if user provided optional size 'N'
# @param data raw input given by user
# @param start offset in case user is 'pagination'
# @return offset to be used by server side functions for 
# pagination
def optional_size(data, start):
    n = data.split(' ')
    size = 10
    if len(n) > 1:
        if n[1].isdigit():
            size = int(n[1])
        else:
            raise TypeError("Non-digit input was provided: ", size)
    start*=size
    return start,str(size + start)


# 'all groups' function. Provides string with necessary information to obtain
# list of currently subscribed groups from server.
# @param user username of current user
# @param data raw input given by user
# @param n current offset (times we have already read the same content)
# @return string to sent to server side 'ag'
def ag(user, data, n):
    n,size = optional_size(data, n)
    groups = get_subscribed_groups(user)
    response = 'ag ' + str(n) + ' ' + size + ' ' + '\5'.join(str(g['group_id']) for g in groups)
    return response

# 'subscribed groups' function. Provides string with necessary information to obtain
# list of all groups from server
# @param user username of current user
# @param data raw input provided by user
# @param n current offset (times we have already read the same content)
# @return string to sent to server side 'sg'
def sg(user, data, n):
    n, size = optional_size(data, n)
    groups = get_subscribed_groups(user)
    # with optional size N of size and offset of n (really need to change variable names)
    # we have output: 'sg 4 7 1\x0520\x052\x0510'
    response = 'sg ' + size + ' ' + str(n) + ' ' + '\5'.join( # DEBUG: size and n might be inverted.
        (str(g['group_id']) + '\5' + str(g['read_count']) for g in groups))
    return response


# 'read group' function. Provides string with necessary information to obtain
# posts in group
# @param username username of current user
# @param data raw input provided by user
# @param gid id of current group
# @param offset current offset (times we have already read the same content)
# @return string to sent to server side 'rg'
def rg(username, data, gid, offset):
    # data.split(' ') -> ['rg','group.name','5']
    data = data.split(' ')
    n = 10 #how many at a time
    if len(data) <= 1:
        raise RuntimeError("No groupname specified")

    if not check_subscription(username, gid):
        return

    if len(data) > 2:
        if n[2].isdigit():
            n = data[2]
        else:
            raise TypeError("Non-digit input was provided: ", n)
    response = 'rg ' + str(n) + ' ' + str(offset) + ' ' + '\5' + str(gid)
    response += get_posts(username, gid)
    return response

# checks if a file already exists on local machine 
# for the current user, creates one if necessary
# @param user username of current user
def check_user(user):
    if user + '.json' not in listdir('./'):
        with open(user + '.json', 'w') as f:
            obj = {'groups': []}
            dump(obj=obj, fp=f, indent=4)

# gets list of current posts
# @param username username of current user
# @param gid group id of group from which to obtain posts
# @return string containing IDs of all posts 
# to attach to server response
def get_posts(username, gid):
    groups = get_subscribed_groups(username)
    response = '\5'
    for g in groups:
        if g['group_id'] == gid:
            for p in g['read_posts']:
                response += '\r\n' + str(p['post_id'])
    return response

# accesses local file to obtain the groups to which 
# the current user is subscribed
# @param uname username of current user
# @return dictionary object containing subscribed groups
def get_subscribed_groups(uname):
    with open(uname + '.json') as f:
        return load(fp=f)['groups']

# obtains information for creation of new posts and formats string 
# to send post information to server
# @param uname username of current user
# @param data raw input given by user
# @param groupid ID of group to which user is posting
# @return formatted string to sent to server side 'p'
def p(uname, data, groupid):
    subject = input('Subject: ')
    content = input('Content: ')

    response = data + ' ' + '\5'.join([str(groupid), uname, subject, content])
    return response


# accesses local user file to 'mark a post as read'
# @param uname username of current user
# @param data raw input provided by user
# @param groupid ID of group to which the post belongs
def r(data, uname, groupid):
    args = data.split(' ')
    if len(args) == 2:
        start = int(args[1])
        end = int(args[1])+1
    elif len(args) == 3:
        start = int(args[1])
        end = int(args[2]) + 1
    l = [i for i in range(start, end)]
    groups = get_subscribed_groups(uname)

    for i in range(len(groups)):
        if groups[i]['group_id'] == groupid:
            for j in groups[i]['read_posts']:
                if j['post_id'] in l:
                    l.remove(j['post_id'])
            for j in l:
                groups[i]['read_posts'].append({'post_id': j})

    with open(uname + '.json', 'w') as f:
        dump({'groups': groups}, fp=f, indent=True)

# accesses local user file to 'subscribe' to groups
# @param uname username of current user
# @param data raw input provided by user
def s(uname, data):
    args = data.split(' ')
    if len(args)==2:
        start = int(args[1])
        end = int(args[1]) + 1
    elif len(args)== 3:
        start = int(args[1])
        end = int(args[2]) + 1
    l = [i for i in range(start, end)]
    groups = get_subscribed_groups(uname)
    x = [] # list of items that are duplicates
    for i in range(len(groups)):
        if groups[i]['group_id'] in l: # add only those that are not already added, prevent duplication
            x.append(groups[i]['group_id'])
    for o in x: #remove groups already in subscribed group from l
        l.remove(o)
    for i in l:
        #add the remaining items
        groups.append({
            'group_id': i,
            'read_count': 0,
            'read_posts': []
        })

    with open(uname + '.json', 'w') as f:
        dump({'groups': groups}, fp=f, indent=4)

# accesses local user file to 'unsubscribe' to groups
# @param uname username of current user
# @param data raw input provided by user
def u(uname, data):
    args = data.split(' ')
    if len(args) == 2:
        start = int(args[1])
        end = int(args[1]) + 1
    elif len(args) == 3:
        start = int(args[1])
        end = int(args[2]) + 1
    l = [i for i in range(start, end)]
    groups = get_subscribed_groups(uname)
    x = [] # groups to be removed
    for i in range(len(groups)):
        #only remove groups that the user is actually subscribed to.
        if groups[i]['group_id'] in l: #add groups to be removed into x, need this because can't erase by index since indices shift on removal
            x.append(groups[i])
    for o in x:
        groups.remove(o)
    with open(uname + '.json', 'w') as f:
        dump({'groups': groups}, fp=f, indent=4)


# checks if current user is a member of group denoted by its ID
# @param username username of current user
# @param gid ID of group of which to check subscription
# @return True if user is a member of group, false otherwise
def check_subscription(username, gid):
    groups = get_subscribed_groups(username)
    for g in groups:
        if g['group_id'] == gid:
            return True
    raise False

# formats string for server to 'read post'
# @param gid ID of group where post belongs
# @param data raw input provided by user
# @return formatted string to send to server side 'rp'
def rp(gid, data):
    return 'rp '+'\5'.join([str(gid),data])

