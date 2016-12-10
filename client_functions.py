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