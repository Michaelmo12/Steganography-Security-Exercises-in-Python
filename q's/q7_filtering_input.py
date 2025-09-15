import re

USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{1,32}$")
PASSWORD_RE = re.compile(r"^[A-Za-z0-9_!@#%^&*+=-]{8,64}$")

def validate_username(u):
    return bool(USERNAME_RE.fullmatch(u))

def validate_password(p):
    return bool(PASSWORD_RE.fullmatch(p))
