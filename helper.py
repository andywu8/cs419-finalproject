from flask import redirect, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            print(session.get("username"))
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function