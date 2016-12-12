from json import load, dump
from os import listdir

NOT_LOGGED_IN = "Not logged in. Please log in before using the forum.\n"
HELP = '''Usage: COMMAND [ARG|SUBCOMMAND] [SUBCOMMAND]
    login USERID\tDetermines which discussion groups you are to and which posts you have read
    help\tPrints this help menu of supported commands and subcommands
    ag [N] [s|u|n|q]\tList the names of all existing discussion groups optional argument N at a time
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
    logout\tLogs out current user'''


def login(username, data):
    username = data.split(' ')[1]
    check_user(username)
    return


def is_logged_in(username):
    return False if username is None else True


def not_logged_in():
    print(NOT_LOGGED_IN)
    print(HELP)


def optional_size(data, start):
    n = data.split(' ')
    size = 10
    if len(n) > 1:
        if n[1].isdigit():
            size = int(n[1])
        else:
            raise TypeError("Non-digit input was provided: ", size)
    return str(size + start)


def ag(user, data, n):
    size = optional_size(data, n)
    groups = get_subscribed_groups(user)
    response = 'ag ' + n + ' ' + size + '\5'.join(str(g['group_id']) for g in groups)
    return response


def sg(user, data, n):
    size = optional_size(data, n)
    groups = get_subscribed_groups(user)
    # with optional size N of size and offset of n (really need to change variable names)
    # we have output: 'sg 4 7 1\x0520\x052\x0510'
    response = 'sg ' + size + ' ' + n + ' ' + '\5'.join(
        (str(g['group_id']) + '\5' + str(g['read_count']) for g in groups))
    return response


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
    response = 'rg ' + n + ' ' + str(offset) + ' ' + '\5' + str(gid)
    response += get_posts(username, gid)
    return response


def check_user(user):
    if user + '.json' not in listdir('./'):
        with open(user + '.json', 'w') as f:
            obj = {'groups': []}
            dump(obj=obj, fp=f, indent=2)


def get_posts(username, gid):
    groups = get_subscribed_groups(username)
    response = '\5'
    for g in groups:
        if g['group_id'] == gid:
            for p in g['read_posts']:
                response += '\r\n' + str(p['post_id'])
    return response


def get_subscribed_groups(uname):
    with open(uname + '.json') as f:
        return load(fp=f)['groups']


def p(uname, data, groupid):
    subject = input('Subject: ')
    content = input('Content: ')

    response = data + ' ' + '\5'.join([groupid, uname, subject, content])
    return response


def r(data, uname, groupid):
    args = data.split(' ')
    start = int(args[1])
    end = int(args[2])
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


def s(uname, data):
    args = data.split(' ')
    start = int(args[1])
    end = int(args[2]) + 1
    l = [i for i in range(start, end)]
    groups = get_subscribed_groups(uname)
    x = []
    for i in range(len(groups)):
        if groups[i]['group_id'] in l:
            x.append(groups[i]['group_id'])
    for o in x:
        l.remove(o)
    for i in l:
        groups.append({
            'group_id': i,
            'read_count': 0,
            'read_posts': []
        })

    with open(uname + '.json', 'w') as f:
        dump({'groups': groups}, fp=f, indent=4)


def u(uname, data, ):
    args = data.split(' ')
    start = int(args[1])
    end = int(args[2])
    l = [i for i in range(start, end)]
    groups = get_subscribed_groups(uname)
    x = []
    for i in range(len(groups)):
        if groups[i]['group_id'] in l:
            x.append(groups[i])
    for o in x:
        groups.remove(o)
    with open(uname + '.json') as f:
        dump({'groups': groups}, fp=f, indent=4)


def check_subscription(username, gid):
    groups = get_subscribed_groups(username)
    for g in groups:
        if g['id'] == gid:
            return True
    raise False

def rp(groupid, data):
    return '\5'.join(['rp',groupid,data])

