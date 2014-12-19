"""
This module provides a simple implementation of hearts. Only a single round
is implemented with left passing.
"""

from random import shuffle

from engine.card_game.card import Card
from engine.card_game.playing_card import create_deck
from engine.core.decorators import game_action
from engine.core.game import Game


class Hearts(Game):
    """
    Hearts is a medium diffuiculty game played with 3 or 4 players.
    """

    def __init__(self):
        super(Hearts, self).__init__()
        self.current_player = None
        self.hearts_broken = False
        self.is_first_turn = True

    def set_up(self):
        all_cards = create_deck()
        shuffle(all_cards)
        self.register(all_cards)


        # Deal out among the players
        while len(all_cards) > 52 % len(self.players):
            for player in self.players:
                card = all_cards.pop()
                if card.number == 2 and card.suit == 'clubs':
                    self.current_player = player

                card.owner = player
                card.face_up = False
                card.set_player_override('face_up', True, player)
                player.hand.push(card)

        # Move any extra cards to the hole.
        while len(all_cards) > 0:
            card = all_cards.pop()
            if card.number == 2 and card.suit == 'clubs':
                pass # TODO: Put in proper logic here
            else:
                self.pocket.push(card)
        self.play_zone.suit = None

    def is_over(self):
        """
        Hearts is over if everybody has played all their cards
        """

        return (len(self.players[0].hand) == 0)


    def winners(self):
        """
        Count up the number of cards in each player's discard zone.
        """

        # TODO: Write this


    def can_play_card(self, player, card):
        """
        Make sure that a player can play a card.
        """

        # Make sure we own the card an it's in our hand
        if card not in player.hand:
            return False

        # Make sure it's our turn.
        if self.current_player != player:
            return False

        # Check for special rules on the first turn
        if self.is_first_turn:
            if (len(self.play_zone) == 0 and
                not (card.number == 2 and card.suit == 'clubs')):
                return False
            if (card.suit == 'hearts' or
                (card.number == 12 and card.suit == 'spades')):
                return False

        # If everybody has already played then we can't play any more
        if len(self.play_zone) >= len(self.players):
            return False

        # Check the card suit (if it's not the leading suit and we have one)
        leading_suit = self.play_zone.suit

        if leading_suit is None:
            if card.suit == 'hearts' and not self.hearts_broken:
                return False
        else:
            if (leading_suit != card.suit and
                len([x for x in player.hand if x.suit == leading_suit]) > 0):
                return False
        return True

    def can_take_trick(self, player):
        """
        Check that a player can take a trick.
        """

        if len(self.play_zone) != len(self.players):
            return False

        # Find the highest card
        valid_cards = [x for x in self.play_zone.get_cards()
                       if x.suit == self.play_zone.suit]
        max_card = None
        max_value = 0
        for card in valid_cards:
            if card.number > max_value:
                max_card = card
                max_value = card.number

        if max_card.owner != player:
            return False

        return True


    @game_action(parameter_types=[{'name': 'card', 'type': Card}],
                 restriction=can_play_card)
    def play_card(self, player, card):
        """
        Play a card from your hand onto the table.
        """

        player.hand.remove(card)
        self.play_zone.add(card)
        card.face_up = True

        if self.play_zone.suit is None:
            self.play_zone.suit = card.suit

        if len(self.play_zone) < len(self.players):
            self.current_player = self.next_player(player)


    @game_action(restriction=can_take_trick)
    def take_trick(self, player):
        """
        Takes a trick, update any internal state if necessary.
        """

        contains_point_card = False
        while len(self.play_zone) > 0:
            card = self.play_zone.pop()
            card.face_up = False
            card.set_player_override("face_up", False, card.owner)
            player.discard.push(card)

            if (card.suit == 'hearts' or
                card.suit == 'spades' and card.number == 12):
                contains_point_card = True

        if not self.hearts_broken and contains_point_card:
            self.hearts_broken = True

        # Check if we need to take anything from the side_zone
        if len(self.pocket) > 0 and contains_point_card:
            player.discard.push_all(self.pcoket.pop_all())

        self.play_zone.suit = None
        self.current_player = player

        if self.is_first_turn:
            self.is_first_turn = False

    def next_player(self, player):
        """
        A simple utility function to get the next player in the turn order.
        """

        player_index = self.players.index(player)
        if player_index == (len(self.players) - 1):
            self.add_transition(['player',self.players[0].game_id])
            return self.players[0]
        else:
            self.add_transition(['player',self.players[player_index + 1].game_id])
            return self.players[player_index + 1]
