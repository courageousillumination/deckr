"""
This module provides the Zone class.
"""

import random

class Zone(object):

    """
    A Zone basically represents a region of the game. A zone has a
    collection of cards, and several other attributes that define how
    the zone interacts with the cards.
    """

    def __init__(self):
        self.game_id = None
        self.cards = []

    def add_card(self, card):
        """
        Add a card to the zone. This is an unorderd operation.
        """

        if card is None or card in self.cards:
            return False
        
        self.cards.append(card)
        return True

    def remove_card(self, card):
        """
        Remove a card from a zone. If the card is not present
        this will return false. Otherwise it will return true.
        """

        if card in self.cards:
            self.cards.remove(card)
            return True
        
        return False

    def push(self, card):
        """
        Push a card on the zone, treating the zone as a stack.
        This is an ordered operation.
        """

        return self.add_card(card)

    def pop(self):
        """
        Pop a card off of the zone. This is an ordered operation.
        """

        if len(self.cards) > 0:
            return self.cards.pop()
        
        return None

    def get_cards(self):
        """
        Get a list of all the cards in this zone.
        """

        return self.cards

    def get_info(self):
        """
        Get a dictionary that defines all the attributes of this
        zone.
        """

        pass

    def shuffle(self):
        """
        Shuffle the cards in this zone.
        """

        random.shuffle(self.cards)

    def get_num_cards(self):
        """
        Get the number of cards in this zone.
        """

        return len(self.cards)

    def __contains__(self, card):
        """
        Check if a card is in this zone.
        """

        return card in self.cards
