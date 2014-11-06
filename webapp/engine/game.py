"""
This module defines everything needed for the base Game class.
"""


def action(restriction=None):
    """
    This is a decorator that can be put around actions in Game subclasses.
    restrictions is an optional function that takes the same arguments as
    the original function and returns a bool. If restrictions returns false
    the action will raise an exception.
    """

    def wrapper(func):
        """
        Part of the wrapper to make the decorator work.
        """

        def inner(*args, **kwargs):
            """
            Yet another part of the decorator.
            """

            if restriction(**kwargs):
                return func(*args, **kwargs)
            else:
                raise RuntimeError
        return inner
    return wrapper


class Game(object):

    """
    A game is one of the core classes of the engine. It contains logic to run
    actions, check the game state, and calculate state transitions that are
    caused by specific actions.
    """

    def __init__(self):
        self.zones = {}
        self.max_players = 0

    def load_config(self, config):
        """
        This will load a game from a configuration_file.
        Somebody else should do the parsing and pass the config a dictionary
        that defines the configuration of the game.
        """

        pass

    def make_action(self, action_name, **kwargs):
        """
        This will try to make an action with the specified
        keyword arguments. It will look at all internal functions
        that have the @action and attempt to run the first one that
        matches. If the action is invalid this could throw an exception.
        """

        pass

    def register(self, objects):
        """
        This function will register objects in the game. Each object will
        be given a unique id (unique within its class). Objects that already
        have an id will not be assigned a new one.
        """

        pass

    def get_object_with_id(self, klass, game_id):
        """
        Gets an internal object of the given class with the given id. If
        the object isn't found this just return None.
        """

        pass

    # Actions after this point should be implemented by subclasses

    def set_up(self):
        """
        This will set up the actual game. This includes dealing cards, setting
        up state, etc. This should be used over __init__.
        """

        pass

    def is_over(self):
        """
        This function will be called after every action to see if the game
        is over.
        """

        pass
