from json import load

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

    # TODO: add check if file exists, file creation if not

    return


def is_logged_in(username):
    return False if username is None else True


def not_logged_in():
    print(NOT_LOGGED_IN)
    print(HELP)


def ag(data, user):
	n = data.split(' ')
    size = len(n)
    #Is the second argument a number?
    if (int(size).isdigit())
        if (size > 1):
            size = n[1]
        else:
            size = 0
    if (size < 0):
        raise
    groups = get_groups(user)
    data = 'ag '.join((str(g['group_id'])+'\5' for g in groups))
    return data


def sg(user):
    groups = get_groups(user)
    data = 'sg '.join((str(g['group_id']).join('\5') for g in groups))
    return data


def get_groups(uname):
    with open(uname + '.json') as f:
        return load(fp=f)['groups']
