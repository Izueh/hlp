from json.encoder import JSONEncoder


class User():
    def __init__(self, user,groups):
        self.user = user
        self.groups = groups


def create_user(json):
    if 'user' in json and 'groups' in json:
        uname = json['user']
        groups = json['groups']
        return User(uname,groups)

    return json


class UserDecoder(JSONEncoder):
    def default(self, o):
        if isinstance(o,User):
            return o.__dict__
        return JSONEncoder.default(o)

