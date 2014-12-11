"""
This module defines the player class.
"""

from engine.core.game_object import GameObject
from engine.mixins.has_zones import HasZones


class Player(GameObject, HasZones):

    """
    This class basically represents a player in the game.
    It contains no logic.
    """

    def __init__(self):
        super(Player, self).__init__()

        self.game_object_type = "Player"
