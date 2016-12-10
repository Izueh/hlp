NOT_LOGGED_IN = "Not logged in. Please log in before using the forum.\n"

def login(username, data):
	username = data.split(' ')[1]

	#TODO: add check if file exists, file creation if not

	return

def is_logged_in(username):
	return False if username==None else True

def not_logged_in():
	print(NOT_LOGGED_IN)
    print(HELP)

def help ():
	# Print supported commands and sub-commands
	print("Usage: COMMAND [ARG|SUBCOMMAND] [SUBCOMMAND]")
	print("login USERID\tDetermines which discussion groups you are to and which posts you have read")
	print("help\tPrints this help menu of supported commands and subcommands")
	print("ag [N] [s|u|n|q]\tList the names of all existing discussion groups optional argument N at a time")
	print("\ts N\tSubscribe to groups by specifying the group number")
	print("\tu N\tUnsubscribe from groups by specifying the group number")
	print("\tn\tList the next N discussion groups. Exits ag command when all N groups displayed")
	print("\tq N\tQuit ag command")
	print("sg [N]\tList the names of all subscribed groups optional argument N at a time")
	print("rg GNAME [N]\tDisplays the status of all posts in group GNAME, optional argument N at a time")
	print("\t[id]\tNumber between 1 and N denoting the post within the list of posts to display")
	print("\t\tn\tDisplays at most N more lines of post content.")
	print("\t\tq\tQuits subcommand [id]")
	print("\tr N [M]\tMarks a post as read. Takes in a number N or range of numbers N - M")
	print("\tn\tLists the next N posts. Exits rg command when all N posts displayed")
	print("\tp\tPost to the group")
	print("\tq\tQuit rg command")
	print("logout\tLogs out current user")

def ag (ngroups, n):
	if (n < 0 || n > ngroups):
		return
