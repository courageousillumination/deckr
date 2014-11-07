"""
This module is the core game_runner. It offers a stateful interface into the
game engine. Any outside service can access running games by making calls
into this module.
"""

# Disable unused arguments. We'll use them. This should be removed later.
# pylint: disable=W0613

# We use globals here because this is a stateful module. It's not super great
# but it's what we've got right now. No need to yell at us for it.
# pylint: disable=W0603

import yaml
import sys
import os.path

CACHE = {}
MAX_ID = 0


def create_game(game_definition):
    """
    Creates a new game. Returns the game id for the
    new game or throws an exception if there was an
    error creating the game.
    """

    global MAX_ID

    game, config = load_game_definition(game_definition)
    game.load_config(config)
    CACHE[MAX_ID] = game

    MAX_ID = MAX_ID + 1

    return MAX_ID - 1


def load_game_definition(game_definition):
    """
    Loads a game definition. A definition minimally consists
    of a game.py that defines the rules and a config.yml that
    defines the configuration. This will return a tuple of a
    configuration dictionary and an instance of the game.
    """

    config_file = open(os.path.join(game_definition, "config.yml"))
    config = yaml.load(config_file)

    if "game_file" not in config or "game_class" not in config:
        raise ValueError("configuration file is missing required attributes.")

    # Add the super directory to the system path
    sys.path.append(game_definition)

    # Explicitly import our game as the game object
    game_module = __import__(config["game_file"])

    # Clean up the system path that we don't care about any more.
    sys.path.remove(game_definition)

    # Get the actual game class out of the module.
    klass = getattr(game_module, config["game_class"])

    return (klass(), config)


def destroy_game(game_id):
    """
    Destroys a game and all of its players, zones, cards,
    etc. Throws an exception if the game doesn't exist.
    """

    del CACHE[game_id]


def get_game(game_id):
    """
    Returns a game based on the id.
    """

    return CACHE.get(game_id, None)


def get_state(game_id):
    """
    Returns the state of the given game.
    """

    return get_game(game_id).get_state()


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

    return game_id in CACHE


def flush():
    """
    Destroys all games
    """

    global CACHE, MAX_ID
    CACHE = {}
    MAX_ID = 0
