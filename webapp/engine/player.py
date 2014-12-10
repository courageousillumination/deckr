"""
This module defines the player class.
"""

from engine.mixins.has_zones import HasZones
from engine.stateful_game_object import StatefulGameObject


class Player(StatefulGameObject, HasZones):

    """
    This class basically represents a player in the game.
    It contains no logic.
    """

    def __init__(self):
        super(Player, self).__init__()

        self.game_object_type = "Player"
