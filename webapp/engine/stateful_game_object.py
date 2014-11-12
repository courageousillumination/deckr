"""
This module defines the StatefulGameObject.
"""


class StatefulGameObject(object):

    """
    A StatefulGameObject is any object in the game that
    has a state that we care about. This superclass overrides
    the __setattr__ to register any state changes with the
    game.
    """

    def __init__(self):
        # This is the ID of **this** object in the game.
        self.game_id = None
        # This is the actual game object that this belongs to.
        self.game = None
        # What attributes shouldn't be tracked (internal attributes mainly)
        self.no_track_attributes = set()

    def __setattr__(self, name, value):

        if (hasattr(self, "game") and
                self.game is not None and
                name not in self.no_track_attributes):
            self.game.add_transition(("set", type(self), self.game_id,
                                      name, value))

        super(StatefulGameObject, self).__setattr__(name, value)
