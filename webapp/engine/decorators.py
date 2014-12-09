"""
This file provides all of the decorators for the engine. Most of these have
to do with game steps and actions.
"""

from engine.exceptions import InvalidMoveException, NeedsMoreInfo


def action(restriction=None):
    """
    This is a decorator that can be put around actions in Game subclasses.
    restrictions is an optional function that takes the same arguments as
    the original function and returns a bool. If restrictions returns false
    the action will raise an InvalidMoveException. This allows you to restrict
    when specifc game events can happen.

    For example if you can only draw when it's your turn you can write

    def is_current_player(self, player):
        return self.current_player = player

    @action(restriction=is_current_player)
    def draw(self, player):
        ...
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            if restriction is None or restriction(*args, **kwargs):
                return func(*args, **kwargs)
            else:
                raise InvalidMoveException("Invalid Move")
        return inner
    return wrapper

def game_step(requires=None):
    """
    TODO: Update this doc string
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            if requires is not None:
                for requirement in requires:
                    if not requirement.verify_kwargs(*args, **kwargs):
                        raise NeedsMoreInfo(requirement)
            return func(*args, **kwargs)
        return inner
    return wrapper
