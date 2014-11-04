def action(restriction = None):
    def wrapper(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return wrapper

class Game(object):

    def __init__(self):
        pass

    def make_action(self, action_id, *args, **kwargs):
        pass

    def set_up(self):
        pass

    def is_over(self):
        pass
    
    def assign_id(self, card, id):
        pass
