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

            return func(*args, **kwargs)
        return inner
    return wrapper


class Game(object):

    """
    A game is one of the core classes of the engine. It contains logic to run
    actions, check the game state, and calculate state transitions that are
    caused by specific actions.
    """

    def __init__(self):
        pass

    def make_action(self, action, **kwargs):
        """
        This will try to make an action with the specified
        keyword arguments. It will look at all internal functions
        that have the @action and attempt to run the first one that
        matches. If the action is invalid this could throw an exception.
        """

        pass

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

    def assign_id(self, card, card_id):
        """
        This is an internal function to assign an id to a card.
        """

        pass
