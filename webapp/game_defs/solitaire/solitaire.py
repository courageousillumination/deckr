"""
This module provides an implementation of a game of Solitaire
"""
from random import shuffle

from engine.card_game.card import Card
from engine.card_game.playing_card import create_deck
from engine.core.decorators import game_action
from engine.core.game import Game
from engine.core.zone import Zone


class Solitaire(Game):
    """
    Solitaire is a simple one player game
    """

    def set_up(self):
        """
        Create cards, and deal them out.
        """

        # Create our deck of cards
        cards = create_deck()
        shuffle(cards)
        self.register(cards)
        self.deck.push_all(cards)
        for i in range(7):
            zone = self.zones["play_zone"+str(i)]
            for _ in range(i+1):
                zone.push(self.deck.pop())
            zone[-1].face_up = True

    def is_over(self):
        """
        Simply checks if you have moved all the cards to the victory zone.
        NOTE: Does not detect if there are no valid moves left.
        """

        victory_zones = [self.zones["victory_zone" + str(i)] for i in range(4)]
        return [len(x) for x in victory_zones].count(14) == 4

    def winners(self):
        """
        Since the only way for the game to end is by victory we just return
        the players list.
        """

        return self.players

    #######################
    # Define game actions #
    #######################

    # pylint: disable=unused-argument

    def draw_restrictions(self, player):
        """
        Make sure there are still cards left somewher to draw.
        """
        return len(self.deck) + len(self.deck_flipped) > 0

    @game_action(restriction = draw_restrictions)
    def draw(self, player):
        """
        Draw a card from the deck. Will also flip over the discard if
        necessary.
        """

        if len(self.deck) == 0:
            cards = self.deck_flipped.pop_all()
            for card in cards:
                card.face_up = False
            self.deck.push_all(cards)
            
        card = self.deck.pop()
        card.face_up = True
        self.deck_flipped.push(card)

    def move_card_restrictions(self, player, card, target_zone):
        """
        Checks the following conditions:

        1) The card is face up.
        2a) If target_zone is a victory zone:
            i) The number is one below.
            ii) The suit is the same.
            iii) The card is at the bottom of the current zone.
        2b) If the target_zone is a play_zone:
            i) The number is one above or a king.
            ii) The suit is the opposite color.
        2c) If the zone is something else it is illegal.

        """

        if not card.face_up:
            return False
        if target_zone.zone_type == 'victory':
            if len(target_zone) == 0:
                if card.number != 1:
                    return False
            elif (target_zone[-1].number != card.number - 1 or
                  target_zone[-1].suit != card.suit):
                return False
            if card.zone[-1] != card:
                return False
        elif target_zone.zone_type == 'play':
            if len(target_zone) == 0:
                if card.number != 13:
                    return False
            elif (target_zone[-1].number != card.number + 1 or
                  target_zone[-1].get_color() == card.get_color()):
                return False
        else:
            return False
        return True

    @game_action(restriction = move_card_restrictions,
                 parameter_types = [{'name': 'card', 'type': Card},
                                    {'name': 'target_zone', 'type': Zone}])
    def move_card(self, player, card, target_zone):
        """
        Move a card from one zone to another, along with all trailing cards
        if possible.
        """

        source_zone = card.zone
        popped_card = None
        cards = []
        while popped_card != card:
            popped_card = source_zone.pop()
            cards.append(popped_card)
        cards.reverse()

        target_zone.push_all(cards)
        last_card = source_zone[-1]
        if last_card is not None and last_card.face_up == False:
            last_card.face_up = True
