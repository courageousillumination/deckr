def create_game(game_definition):

    
    """
    Creates a new game. Returns the game id for the
    new game or throws an exception if there was an
    error creating the game.
    """
    
    pass

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


def get_state(game_id):
    """
    Returns the state of the given game. 
    """
    
    pass

def add_player(game_id):
    """
    Adds a player to the given game, and returns the 
    player id of the newly created player.
    """
    
    pass

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
    
    pass
