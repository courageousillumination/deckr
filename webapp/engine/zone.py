"""
This module provides the Zone class.
"""

import random

from engine.game_object import GameObject


class Zone(GameObject):

    """
    A Zone basically represents a region of the game. A zone has a
    collection of cards, and several other attributes that define how
    the zone interacts with the cards. The constructor can take in an optional
    dictonary that defines specific attributes to be set on the zone.
    """

    def __init__(self, config=None):
        super(Zone, self).__init__()
        self.region_id = None
        self.cards = []

        if config is None:
            config = {}

        self.stacked = config.get('stacked', False)
        self.name = config.get('name', '')
        self.zone_type = config.get('zone_type', '')
        self.owner = None

    def add_card(self, card):
        """
        Add a card to the zone. This is an unorderd operation.
        """

        if card is None or card in self.cards:
            return False

        self.cards.append(card)

        if self.game is not None:
            self.game.add_transition(("add",
                                      card.game_id,
                                      self.game_id))

        card.zone = self
        return True

    def remove_card(self, card):
        """
        Remove a card from a zone. If the card is not present
        this will return false. Otherwise it will return true.
        """

        if card in self.cards:
            self.cards.remove(card)
            if self.game is not None:
                self.game.add_transition(("remove", card.game_id))
            card.zone = None
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
            card = self.cards.pop()
            if self.game is not None:
                self.game.add_transition(("remove", card.game_id))
            card.zone = None
            return card

        return None

    def peek(self):
        """
        Peek at the top card of a zone.
        This is an ordered operation.
        """

        if len(self.cards) > 0:
            return self.cards[-1]

        return None

    def get_cards(self):
        """
        Get a list of all the cards in this zone.
        """

        return self.cards

    def set_cards(self, cards):
        """
        Sets the list of all cards. Sometimes faster to do than
        push each individual one.
        """

        # Remove all current cards
        while len(self.cards) > 0:
            self.pop()

        # Since we're pushing onto a stack we actually need to reverse
        # these cards.
        cards.reverse()

        # Add all the new cards
        for card in cards:
            self.push(card)

    def get_info(self):
        """
        Get a dictionary that defines all the attributes of this
        zone.
        """

        info = {}
        for key in ["stacked"]:
            info[key] = getattr(self, key)

        return info

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
