
"""
This module provides an implementation of Magic: The Gathering.
"""

from engine.game import Game


class Magic(Game):
    """
    Magic: The Gathering.
    """

    def __init__(self):
        super(Magic, self).__init__()


    ##################
    # Base functions #
    ##################

    def set_up(self):
        pass

    def is_over(self):
        pass

    def winners(self):
        pass
