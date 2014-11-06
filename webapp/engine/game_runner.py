"""
This module is the core game_runner. It offers a stateful interface into the
game engine. Any outside service can access running games by making calls
into this module.
"""

# Disable unused arguments. We'll use them. This should be removed later.
# pylint: disable=W0613


def create_game(game_definition):
    """
    Creates a new game. Returns the game id for the
    new game or throws an exception if there was an
    error creating the game.
    """

    return 0


def destroy_game(game_id):
    """
    Destroys a game and all of its players, zones, cards,
    etc. Throws an exception if the game doesn't exist.
    """

    pass


def get_game(game_id):
    """
    Returns a game based on the id
    """

    return 0


def get_state(game_id):
    """
    Returns the state of the given game.
    """

    return {}


def add_player(game_id):
    """
    Adds a player to the given game, and returns the
    player id of the newly created player.
    """

    return 0


def make_action(game_id, *args, **kwargs):
    """
    Makes an action in the game. Can throw an IllegalAction
    exception.
    """

    pass


def has_game(game_id):
    """
    Returns true if there is a game with the given id and False
    otherwise.
    """

    return False


def flush():
    """
    Destroys all games
    """

    pass
