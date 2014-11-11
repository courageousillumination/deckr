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

    class RegionEnum(Enum):
        deck = 1
        victory =2
        play = 3

    """
    Solitaire is a simple one player game
    """

    def set_up(self):
        """
        Just set the setup variable, and make sure the phase
        is restricted.
        """

        self.victory_region = Region(RegionEnum.victory)
        self.play_region = Region(RegionEnum.play)
        self.deck_region = Region(RegionEnum.deck)

        for i in range (0,3):
            self.victory_region.add_zone(Zone(True))
            
        for i in range (0,6):
            self.play_regions.add_zone(Zone())

        self.deck_region.add_zone(Zone(True))
        self.deck_region.add_zone(Zone(False))

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

    def restrictions(self, zoneA, zoneB, cards_to_move):
        """
        Must play same color, lower number.
        """

        cardA = zoneA.get_cards[zoneA.get_num_cards() - cards_to_move - 1]
        cardB = zoneB.peek()

        # We can move cards between the decks
        if(zoneB.region_id == RegionEnum.deck):
            return False

        # victory zone restrictions:
        # must play an ace if empty
        if(zoneB.region_id == RegionEnum.victory):
            if(len(zoneB) != 0):
                return cardA.get("value") == 13
            else:
                if cardA.get("value") == cardB.get("value") - 1:
                    return cardA.get("suit") == cardB.get("suit")

        # We know zone b in the in play region, so if it's empty, we can do anything.
        if(len(zoneB) == 0):
            return True

        return compare_color(cardA, cardB) and cardA.get("value") == cardB.get("value") - 1

    def compare_color(cardA, cardB):
        if cardA.get("suit") == Suit.hearts or cardA.get("suit") == Suit.diamonds:
            return cardA.get("suit") == Suit.hearts or cardB.get("suit") == Suit.diamonds

        if cardA.get("suit") == Suit.spades or cardA.get("suit") == Suit.clubs:
            return cardB.get("suit") == Suit.spades or cardB.get("suit") == Suit.clubs

    @action(restriction=restrictions)
    def move_cards(self, zoneA, zoneB, cards_to_move):
        """
        Move the top card from one zone to another.
        """
        for i in range(1, cards_to_move):
            zoneB.push(zoneA.get_cards[cards_to_move-i])

    @action(restriction=restrictions)
    def flip_deck(self):
        pass
    
