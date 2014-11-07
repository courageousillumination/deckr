"""
This module defines the GameObject.
"""


class GameObject(object):

    """
    A GameObject is any object in the game.
    """

    def __init__(self):
        # This is the ID of **this** object in the game.
        self.game_id = None
        # This is the actual game object that this belongs to.
        self.game = None
