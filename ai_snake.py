
AI_STATE = False


def check_ai(func):
    def wrapper(*args, **kwargs):
        if not AI_STATE:
            return func(*args, **kwargs)
    return wrapper
