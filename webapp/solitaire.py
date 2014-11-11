"""
This module provides an implementation of a game of Solitaire
"""

from engine.game import Game, action
from enum import Enum

class Solitaire(Game):

    class Suit(Enum):
            hearts = 1
            diamonds = 2
            clubs = 3
            spades = 4

    """
    Solitaire is a simple one player game
    """

    def set_up(self):
        """
        Just set the setup variable, and make sure the phase
        is restricted.
        """

        self.victory_region = Region()
        self.play_region = Region()
        self.deck_region = Region()

        for i in range (0,3):
            self.victory_region.add_zone(Zone(True))
            
        for i in range (0,6):
            self.play_regions.add_zone(Zone())

        self.deck_region.add_zone(Zone(True))
        self.deck_region.add_zone(Zone(True))

        for i in Suit:
            for j in range(1,13):
                self.deck_region[1].add_card(Card({"suit": i, "value": j}))

        self.deck_region[1].shuffle()

        for pair in zip(play_region.get_zones(), range(1,8)):
            deal_cards(self.deck_region.get_zones[1], pair[0], pair[1])

        self.register(self.deck_region)
        self.register(self.play_region)
        self.register(self.victory_region)

        self.register(self.deck_region.get_zones())
        self.register(self.play_region.get_zones())
        self.register(self.victory_region.get_zones())
        self.register(self.deck_region.get_zones[1].get_cards())

        self.is_setup = True
        self.phase = "restricted"

    def deal_cards(deck, zone, num_to_deal):
        for i in range(1, num_to_deal):
            zone.add_card(deck.pop())


    def is_over(self):
        """
        Just looks at the internal over variable.
        """

        return self.over

    def winners(self):
        """
        Returns the internal winners_list.
        """

        return self.winners_list

    def restrictions(self, player_id):
        """
        A simple restriction.
        """

        return self.phase != "restricted"

    @action(restriction=None)
    def win(self, player_id):
        """
        If we make this action we win the game.
        """

        self.winners_list.append(player_id)
        self.over = True

    @action(restriction=None)
    def lose(self, player_id):  # pylint: disable=W0613
        """
        If we make this action then we lose.
        """

        self.over = True

    @action(restriction=restrictions)
    def restricted_action(self, player_id):
        """
        This will win, if the phase isn't restricted.
        """

        self.winners_list.append(player_id)
        self.over = True
