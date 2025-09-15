class User:
    def __init__(self, username, roles):
        self.username = username
        self.roles = set(roles)

class Resource:
    def __init__(self, name, required_roles):
        self.name = name
        self.required_roles = set(required_roles)

def can_access(user, res):
    return bool(user.roles & res.required_roles)
