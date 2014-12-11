"""
This module defines the GameObject.
"""


class GameObject(object):

    """
    A GameObject is any object in the game.
    """

    def __init__(self):
        super(GameObject, self).__init__()
        # This is the ID of **this** object in the game.
        self.game_id = None
        # This is the actual game object that this belongs to.
        self.game = None
        # game_attributes should be a set of all attributes that we care
        # about including in the state.
        self.game_attributes = set()

    def serialize(self):
        """
        Converts this object into something that is somewhat useful.
        """

        pass
