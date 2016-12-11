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


def optional_size(line, start):
    n = line.split(' ')
    size = 10
    if len(n) > 1:
        if n[1].isdigit():
            size = int(n[1])
        else:
            raise TypeError("Non-digit input was provided: ", size)
    return str(size + start)


def ag(user, line, n):
    size = optional_size(line, n)
    groups = get_groups(user)
    data = 'ag ' + n + ' ' + size + '\5'.join(str(g['group_id']) for g in groups)
    return data


def sg(user, line, n):
    size = optional_size(line, n)
    groups = get_groups(user)
    data = 'sg ' + str(n) + ' ' + size + ' ' + '\5'.join((str(g['group_id']) for g in groups))
    return data

def rg(line, user, n):
    n = line.split(' ')
    size = 10
    if len(n) <= 1:
        raise RuntimeError("No groupname specified")

    gname = gname + n[1]
    gid = check_group(gname)
    if len(n) > 2:
        if n[2].isdigit():
            size = int(n[2])
        else:
            raise TypeError("Non-digit input was provided: ", size)
    data = 'rg ' + size + ' ' + n + ' ' + '\5' + gid
    data += get_posts
    return data

def check_user(user):
    if user + '.json' not in listdir('./'):
        with open(user + '.json', 'w') as f:
            obj = {'groups': []}
            dump(obj=obj, fp=f, indent=2)

def get_posts(uname, gname):
    groups = get_groups(uname)
    data = '\5'
    for g in groups:
        if g['group_name'] == gname:
            for p in g['read_posts']:
                data += '\r\n' + p['post_id']
    return data

def get_groups(uname):
    with open(uname + '.json') as f:
        return load(fp=f)['groups']

def p(uname,query,groupid,subject,content):
    data = '\5'.join([query,groupid,uname,subject,content])
    return data






def check_group(uname, gname):
    groups = get_groups(uname)
    for g in groups:
        if g['group_name'] == gname:
            return g['group_id']
        else:
            raise ValueError("Not subscribed to group: ", gname)