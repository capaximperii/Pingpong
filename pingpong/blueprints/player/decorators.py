from functools import wraps
from flask import redirect
from flask_login import current_user


def is_authenticated():
    """
    Check if a user is signed in before accessing protected API.

    :return: Function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect('/denied')
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def anonymous_required():
    """
    Check if a user is not already signed in before accessing login again.

    :return: Function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if  current_user.is_authenticated:
                return redirect('/denied')
            return f(*args, **kwargs)

        return decorated_function

    return decorator
