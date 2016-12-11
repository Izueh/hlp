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

    # TODO: add check if file exists, file creation if not

    return


def is_logged_in(username):
    return False if username is None else True


def not_logged_in():
    print(NOT_LOGGED_IN)
    print(HELP)

def optional_size(line):
	n = line.split(' ')
    size = 10
    if (len(n) > 1):
		if(n[1].isdigit()):
       		size = int(n[1])
       	else:
       		raise TypeError("Non-digit input was provided: ", size)
    return str(size)

def ag(line, user):
	size = optional_size(line)
    groups = get_groups(user)
    data = 'ag ' + size + (str(g['group_id']).join('\5') for g in groups)
    return data


def sg(line, user):
	size = optional_size(line)
def sg(user, query):
    groups = get_groups(user)
    data = 'sg ' + size + ' '+ '\5'.join((str(g['group_id']) for g in groups))
    return data


def check_user(user):
    if user + '.json' not in listdir('./'):
        with open(user + '.json', 'w') as f:
            obj = {'groups': []}
            dump(obj=obj, fp=f, indent=2)


def get_groups(uname):
    with open(uname + '.json') as f:
        return load(fp=f)['groups']
