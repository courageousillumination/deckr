"""
This module defines the Card class.
"""

from engine.stateful_game_object import StatefulGameObject

class Card(StatefulGameObject):

    """
    A Card represents a single instance of a card in the game.
    This class doesn't really have any logic associated with it
    and will mainly act as a container for data about the card.
    """

	def __init__(attributes):
		self.attributes = attributes

	def get(value):
		return self.attributes["value"]

	def set(value, new_value):
		self.attributes["value"] = new_value
