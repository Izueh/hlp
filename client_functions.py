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
    response = 'sg ' + size + ' ' + n + ' ' + '\5'.join((str(g['group_id']) + '\5' + str(g['read_count']) for g in groups))
    return response


def rg(data, user, n):
    n = data.split(' ')
    size = 10
    gname = ''
    if len(n) <= 1:
        raise RuntimeError("No groupname specified")

    gname = gname + n[1]
    gid = check_group(gname)
    if len(n) > 2:
        if n[2].isdigit():
            size = int(n[2])
        else:
            raise TypeError("Non-digit input was provided: ", size)
    response = 'rg ' + size + ' ' + n + ' ' + '\5' + gid
    response += get_posts
    return response


def check_user(user):
    if user + '.json' not in listdir('./'):
        with open(user + '.json', 'w') as f:
            obj = {'groups': []}
            dump(obj=obj, fp=f, indent=2)


def get_posts(uname, gname):
    groups = get_subscribed_groups(uname)
    data = '\5'
    for g in groups:
        if g['group_name'] == gname:
            for p in g['read_posts']:
                response += '\r\n' + p['post_id']
    return response


def get_subscribed_groups(uname):
    with open(uname + '.json') as f:
        return load(fp=f)['groups']


def p(uname, data, groupid, subject, content):
    response = '\5'.join([data, groupid, uname, subject, content])
    return response


def r(data, uname, group):
    posts = data.split(' ')[1].split('-')
    if posts == 1:
        groups = get_subscribed_groups(uname)
        for i in range(len(groups)):
            if group[i]['group_id'] == group:
                groups[i]['read_count'] += 1
                for p in groups[i]['read_posts']:
                    if p['post_id'] == posts[0]:
                        return
                groups['read_post'].append({'post_id': posts[0]})
                with open(uname + '.json', 'w') as f:
                    dump({'groups': groups}, fp=f)

    elif posts == 2:
        groups = get_subscribed_groups(uname)
        for i in range(len(groups)):
            if groups[i]['group_id'] == group:
                x = []
                for j in range(len(groups[i]['read_posts'])):
                    if groups[i]['read_posts'][j]['post_id'] != posts[0] \
                            and int(posts[0]) < groups[i]['read_posts'][j]['post_id'] < int(posts[1]):
                        x.append(groups[i]['read_posts'][j]['post_id'])
                    groups[i]['read_count'] += len(x)
                for num in x:
                    groups[i]['read_posts'].append({'post_id': num})
                    with open(uname + '.json', 'w') as f:
                        dump({'groups': groups}, fp=f)


def s(uname, groupid, data):
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


def u(uname, data, groupid):
    args = data.split(' ')
    start = int(args[1])
    end = int(args[2])
    l = [i for i in range(start, end)]
    groups = get_subscribed_groups(uname)
    x=[]
    for i in range(len(groups)):
        if groups[i]['group_id'] == groupid:
            for j in range(len(groups[i]['read_posts'])):
                if groups[i]['read_posts'][j]['post_id'] in l:
                    x.append(groups[i]['read_posts'][j])
            for o in x:
                groups[i]['read_posts'].remove(o)

    with open(uname + '.json', 'w') as f:
        dump({'groups': groups}, fp=f, indent=4)


def check_group(uname, gname):
    groups = get_subscribed_groups(uname)
    for g in groups:
        if g['group_name'] == gname:
            return g['group_id']
        else:
            raise ValueError("Not subscribed to group: ", gname)

