"""
This module defines the Card class.
"""

from engine.core.game_object import GameObject


class Card(GameObject):

    """
    A Card represents a single instance of a card in the game. Not much logic
    is associated with this class, instead it is simply defines what attributes
    a card has. These are:
        * front_face: The front face of the card.
        * back_face: The back face of the card.
        * face_up: Tracks if the card is face up or not.
    """

    def __init__(self):
        super(Card, self).__init__()

        self.front_face = None
        self.back_face = None
        self.face_up = False
        self.game_object_type = 'Card'
        self.game_attributes.add('front_face')
        self.game_attributes.add('back_face')
        self.game_attributes.add('face_up')
