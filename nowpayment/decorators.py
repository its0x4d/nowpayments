# create a decorator to check if a function has a variable called "jwt"

from functools import wraps


def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0].jwt_token:
            raise ValueError("This method requires a JWT token. Set it using `jwt_token=TOKEN` in NowPayments class.")
        return func(*args, **kwargs)
    return wrapper
