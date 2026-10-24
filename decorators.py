from functools import wraps

# Decorator to handle input errors for functions
def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as error:
            message = str(error)
            if isinstance(error, KeyError):
                message = message.strip("'")
            return message or "Enter the argument for the command."

    return inner
