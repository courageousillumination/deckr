
"""
This module provides an implementation of a game of Dominion
"""

import math
import random

from engine.game import action, Game, game_step


def turn_face_up(cards):
    for card in cards:
        card.face_up = True

class Dominion(Game):
    """
    Dominion is a more complex card game.
    """

    def __init__(self):
        super(Dominion, self).__init__()

        self.current_phase = None
        self.current_player = None
        self.is_set_up = False

    ##################
    # Base functions #
    ##################

    def set_up(self):
        """
        Set up does the following things:

        * Selects 10 kingdom cards at random and distributes them into the
          kingdom piles.
        * Distribute curses, victory points, and treasures.
        * Gives each player a starting hand.
        * Sets the current player to be the first player to join the game.
        """

        if self.is_set_up:
            return

        # Cards that are part of every game
        cards_to_zones = [('Curse', 'curses', max((len(self.players) - 1)* 10, 0)),
                          ('Estate', 'victory0', 12),
                          ('Duchy', 'victory1', 12),
                          ('Province', 'victory2', 12),
                          ('Copper', 'treasure0', 60 - 7 * len(self.players)),
                          ('Silver', 'treasure1', 40),
                          ('Gold', 'treasure2', 30),
                          ]

        # Select 10 random kindom cards
        all_kingdom_cards = [x["name"] for x in self.card_set.all_cards() if
                             x["kingdom_card"]]
        kingdom_cards = random.sample(all_kingdom_cards, 10)
        kingdom_cards = [(name, 'kingdom' + str(i), 10)
                         for i, name in enumerate(kingdom_cards)]
        # Combine the base cards and the kingdom cards to get the kingdom
        all_cards = cards_to_zones + kingdom_cards

        for card, zone, num in all_cards:
            cards = self.card_set.create(card, num)
            turn_face_up(cards)
            self.zones[zone].set_cards(cards)
            self.register(cards)

        # Give each player a deck
        for player in self.players:
            deck = (self.card_set.create("Copper", 7) +
                    self.card_set.create("Estate", 3))
            random.shuffle(deck)
            player.deck.set_cards(deck)
            self.register(deck)
            # We can resue the clean up step here
            self.clean_up(player)

        self.current_phase = "action"
        self.current_player = self.players[0]

        is_set_up = True

    def is_over(self):
        """
        This checks for the two win conditions:

        1) Provinces run out (stored in victory2)
        2) Three of any supply pile run out
        """

        if self.victory2.get_num_cards() == 0:
            return True

        supply_zones = [x for x in self.zones.values()
                        if x.zone_type == 'supply' and x.get_num_cards() == 0]
        if len(supply_zones) >= 3:
            return True
        return False


    def winners(self):
        """
        Count up victory points for each player and return a list of all
        the players that are tied for the maximum
        """

        def player_score(player):
            """
            Count the score of a specific player.
            """
            score = 0
            all_cards = (player.hand.get_cards() + player.discard.get_cards() +
                         player.deck.get_cards())
            for card in (all_cards):
                if ("victory" in card.card_type or
                    "curse" in card.card_type):
                    # We resolve the gardens manually here
                    if card.name == "Gardens":
                        score += math.floor(len(all_cards) / 4)
                    else:
                        score += card.victory_points
            return score

        max_score = float("-inf")
        max_players = None
        for player in self.players:
            score = player_score(player)
            if score > max_score:
                max_score = score
                max_players = [player]
            elif score == max_score:
                max_players.append(player)

        return max_players

    #######################
    # Action Restrictions #
    #######################

    def play_card_restrictions(self, player, card):
        """
        This will check the following requirements:

        1) It's your turn
        2) The card you're playing is in your hand.
        3) If it's an action, then the phase is action and you have actions.
        4) If it's a treasure make sure the phase is buy.
        """

        if self.current_player != player:
            return False
        if card not in player.hand:
            return False
        if self.current_phase == "action":
            if "action" not in card.card_type:
                return False
            if player.num_actions <= 0:
                return False
        if self.current_phase == "buy" and "treasure" not in card.card_type:
            return False
        return True

    def buy_restrictions(self, player, buy_zone):
        """
        This will check the following:

        1) It's your turn and the phase is "buy"
        2) The zone is a supply zone and has cards remaining.
        3) You have a buy.
        4) You have enough money
        """

        if self.current_player != player or self.current_phase != "buy":
            return False
        if buy_zone.zone_type != 'supply' or buy_zone.get_num_cards() == 0:
            return False
        if player.num_buys <= 0:
            return False
        if player.money_pool < buy_zone.peek().cost:
            return False
        return True

    def next_phase_restrictions(self, player):
        """
        You can only go onto the next phase if it's your turn.
        """

        if self.current_player != player:
            return False
        return True

    ###########
    # Actions #
    ###########

    @action(restriction = play_card_restrictions)
    def play_card(self, player, card):
        """
        This will mainly move the card into the play zone, update the number
        of actions and then call the resolve function on the card.
        """

        player.hand.remove_card(card)
        player.play_zone.add_card(card)
        card.face_up = True
        if "action" in card.card_type:
            player.num_actions -= 1
        self.resolve(player, card)

    @action(restriction = buy_restrictions)
    def buy(self, player, buy_zone):
        """
        This will simply move the card from the buy zone to the player's
        discard zone, and update the values for the player.
        """

        card = buy_zone.pop()
        player.discard.push(card)
        player.num_buys -= 1
        player.money_pool -= card.cost

    @action(restriction = next_phase_restrictions)
    def next_phase(self, player):
        """
        This function will be called whenever a player is done with their phase.
        If they are finishing the action step it will move to the buy; if
        they are finishing the buy step it will call the clean up step and
        then update the player.
        """

        if self.current_phase == "action":
            self.current_phase = "buy"
        elif self.current_phase == "buy":
            self.clean_up(player)
            self.current_phase = "action"
            self.current_player = self.next_player(self.current_player)

    #####################
    # Utility Functions #
    #####################

    def get_next_card(self, player):
        """
        This function will get the next card for a specifc player. It will
        reshuffle if needed, and returns None if it can't possibly get another
        card.
        """

        if player.deck.get_num_cards() == 0:
            if player.discard.get_num_cards() == 0:
                return None
            # Trigger a reshuffle
            while player.discard.get_num_cards() > 0:
                card = player.discard.pop()
                card.face_up = False
                card.set_value("face_up", False, player)
                player.deck.push(card)
            player.deck.shuffle()
        return player.deck.pop()

    def resolve(self, player, card):
        """
        This simply passes off to individual resolve functions.
        """

        fun_name = "resolve_"+'_'.join(card.name.lower().split(' '))
        getattr(self, fun_name)(player, card)

    def next_player(self, player):
        """
        Gets the next player after a specific player in the turn order.
        """

        player_index = self.players.index(player)
        if player_index == (len(self.players) - 1):
            return self.players[0]
        else:
            return self.players[player_index + 1]

    def pluses(self, player, num_cards = 0, num_actions = 0,
               num_buys = 0, num_coin  = 0):
        """
        This is used for adding cards, actions, and buys in one function.
        """

        for _ in range(num_cards):
            self.draw(player)
        player.num_actions += num_actions
        player.num_buys += num_buys
        player.money_pool += num_coin

    def for_each_other_player(self, player, fun, **kwargs):
        """
        Runs fun for each other player. Player will be the first positional
        argument and any keyword arguments will be passed along.
        """

        for p in self.players:
            if p != player:
                fun(player, **kwargs)

    def find_in_hand(self, player, test):
        """
        Test to see if a players hand contains a card specified by test.
        """

        for card in player.hand.get_cards():
            if test(card):
                return card
        return None

    ###################
    # Game Step Tests #
    ###################

    # pylint: disable=unused-argument

    def cards_in_hand(self, player, cards, min_cards, max_cards, test = None, **kwargs):
        if not isinstance(cards, list):
            return False

        if test is not None:
            for card in cards:
                if not test(card):
                    return False

        if (min_cards is not None and len(cards) < min_cards or
            max_cards is not None and len(cards) > max_cards):
            return False

        for card in cards:
            if card not in player.hand:
                return False

        return True

    def gain_test_wrapper(self, player, gain_from_zone, gain_test, **kwargs):
        # We can only gain a card if it's there
        if gain_from_zone.get_num_cards() == 0:
            return False

        return gain_test(player, gain_from_zone.peek(), **kwargs)

    def trash_test_wrapper(self, player, card, trash_test, **kwargs):
        if (not self.card_in_hand(card, player) or not trash_test(card)):
            return False
        return True

    def militia_card_test(self, player, cards, **kwargs):
        for card in cards:
            if card not in player.hand:
                return False
        if len(player.hand.get_cards()) - len(cards) != 3:
            return False
        return True

    def simple_test(self, *args, **kwargs):
        return True

    def card_in_hand(self, player, card, **kwargs):
        return card in player.hand

    def in_possible_cards(self, player, card, possible_cards, **kwargs):
        return card in possible_cards

    def victory_card_in_hand(self, player, card, **kwargs):
        return card in player.hand and "victory" in card.card_type

    def costs_up_to_x(self, player, card, max_cost, **kwargs):
        return card.cost <= max_cost

    def costs_up_to_x_more(self, player, card, other_card, max_delta, **kwargs):
        return card.cost <= other_card.cost + max_delta

    def card_type_contians(self, player, card, card_type, **kwargs):
        return card_type in card.card_type

    ##############
    # Game Steps #
    ##############
    @game_step(requires=None)
    def draw(self, player, **kwargs):
        """
        Draws a card for a single player.
        """
        card = self.get_next_card(player)
        if card is None:
            return
        card.set_value("face_up", True, player)
        player.hand.push(card)

    @game_step(requires=None)
    def draw_cards(self, player, num_cards, **kwargs):
        """
        Draws a specific number of cards. This is used by Cellar.
        """

        for _ in range(num_cards):
            self.draw(player)
        return num_cards

    @game_step(requires=None)
    def clean_up(self, player):
        """
        Execute the clean up phase. This involves resetting all values
        discarding all cards and drawing a new hand.
        """

        # Move everything from the play zone
        while player.play_zone.get_num_cards() > 0:
            player.discard.push(player.play_zone.pop())

        # Move everything from the hand
        while player.hand.get_num_cards() > 0:
            card = player.hand.pop()
            player.discard.push(card)
            card.face_up = True

        # Draw 5 more
        for _ in range(5):
            self.draw(player)

        # Reset all variables
        player.money_pool = 0
        player.num_actions = 1
        player.num_buys = 1

    @game_step(requires=[("cards", "Cards", cards_in_hand)])
    def discard_cards(self, player, cards, **kwargs):
        """
        Discard all cards, and returns the number of cards discarded.
        """

        for card in cards:
            player.hand.remove_card(card)
            player.discard.add_card(card)
            card.face_up = True
        return len(cards)

    @game_step(requires=[("cards", "Cards", cards_in_hand)])
    def trash_cards(self, player, cards, **kwargs):
        """
        Trash a list of cards. The only requirement is that these cards
        are in your hand.
        """

        for card in cards:
            player.hand.remove_card(card)
            self.trash.add_card(card)
            card.face_up = True
        return cards

    @game_step(requires=[("card", "Card", trash_test_wrapper)])
    def trash_card(self, player, card, trash_test, **kwargs):
        """
        Trash a specific card. A test can be passed in and the card must
        satisfy that test.
        """

        self.trash_cards(player, [card])
        return card

    @game_step(requires=[("gain_from_zone", "Zone", gain_test_wrapper)])
    def gain(self, player, gain_from_zone, gain_test, **kwargs):
        """
        This can be used to gain a card. A gain_test should be passed in that
        verifies that the card is legit.
        """

        card = gain_from_zone.pop()
        if card is not None:
            player.discard.push(card)

    @game_step(requires=[("flag", "Bool", simple_test)])
    def discard_deck(self, player, flag, **kwargs):
        if flag:
            while player.deck.get_num_cards() > 0:
                card = player.deck.pop()
                card.face_up = True
                card.set_value("face_up", True, player)
                player.discard.push(card)

    @game_step(requires=[("cards", "Cards", militia_card_test)])
    def discard_down_to_3(self, player, cards, **kwargs):
        for card in cards:
            player.hand.remove_card(card)
            player.discard.add_card(card)
            card.face_up = True
        return len(cards)

    @game_step(requires=[("card", "Card", card_in_hand)])
    def select_throne_room_card(self, player, card, **kwargs):
        """
        This is a simple resolution of the Throne Room card.
        """

        player.hand.remove_card(card)
        player.play_zone.add_card(card)
        card.face_up = True
        self.resolve(player, card)
        self.resolve(player, card)

    @game_step(requires=[("discard", "Bool", simple_test)])
    def spy_step(self, player, other_player, revealed_card, discard, **kwargs):
        if discard:
            other_player.discard.push(revealed_card)
        else:
            revealed_card.face_up = False
            revealed_card.set_value("face_up", False, other_player)
            other_player.deck.push(revealed_card)

    @game_step(requires=[("card", "Card", in_possible_cards)])
    def thief_trash(self, player, card, possible_cards, **kwargs):
        card.zone.remove_card(card)
        self.trash.push(card)

    @game_step(requires=[("steal", "Bool", lambda *args, **kwargs: True)])
    def thief_steal(self, player, card, steal, **kwargs):
        if steal:
            card.zone.remove_card(card)
            player.discard.push(card)
        self.clear_keyword_argument('card')
        self.clear_keyword_argument('steal')

    @game_step(requires=[("keep", "Bool", lambda *args, **kwargs: True)])
    def library_step(self, player, next_card, keep, **kwargs):
        """
        This will only be called next_card is an action card.
        """

        if not keep:
            player.hand.remove_card(next_card)
            player.discard.push(next_card)
            next_card.face_up = True

        self.clear_keyword_argument('keep')
        while player.hand.get_num_cards() < 7:
            next_card = self.get_next_card(player)
            if next_card is None:
                return

            player.hand.push(next_card)
            next_card.set_value("face_up", True, player)
            if "action" in next_card.card_type:
                # If it's an action we call this again and wait for the user
                # to pass in a value
                self.add_step(player,
                              self.library_step,
                              kwargs = {"next_card": next_card})
                return

    @game_step(requires=[("card", "Card", victory_card_in_hand)])
    def put_back_victory_card(self, player, card, **kwargs):
        player.hand.remove_card(card)
        player.deck.push(card)
        card.face_up = False
        card.set_value("face_up", False, player)

    ###############################
    # Individual Card Resolutions #
    ###############################

    def resolve_copper(self, player, card):
        self.pluses(player, num_coin=1)

    def resolve_silver(self, player, card):
        self.pluses(player, num_coin=2)

    def resolve_gold(self, player, card):
        self.pluses(player, num_coin=3)

    def resolve_moat(self, player, card):
        self.pluses(player, num_cards=2)

    def resolve_chapel(self, player, card):
        self.add_step(player,
                      self.trash_cards,
                      kwargs = {'max_cards': 4,
                                'min_cards': None})

    def resolve_cellar(self, player, card):
        self.pluses(player, num_actions=2)
        self.add_step(player,
                      self.discard_cards,
                      save_result_as = "num_cards",
                      kwargs = {'min_cards': None,
                                'max_cards': None})
        self.add_step(player, self.draw_cards)

    def resolve_chancellor(self, player, card):
        self.pluses(player, num_coin=2)
        self.add_step(player, self.discard_deck)

    def resolve_village(self, player, card):
        self.pluses(player, num_cards=1, num_actions=2)

    def resolve_woodcutter(self, player, card):
        self.pluses(player, num_coin=2, num_buys=1)

    def resolve_workshop(self, player, card):
        self.add_step(player,
                      self.gain,
                      kwargs = {'gain_test': self.costs_up_to_x,
                                'max_cost': 4})

    def resolve_smithy(self, player, card):
        self.pluses(player, num_cards=3)

    def resolve_council_room(self, player, card):
        self.pluses(player, num_cards=4, num_buys=4)

        self.for_each_other_player(player,
                                   lambda x: self.pluses(x, num_cards=1))

    def resolve_laboratory(self, player, card):
        self.pluses(player, num_cards=2, num_actions=1)

    def resolve_festival(self, player, card):
        self.pluses(player, num_actions=2, num_buys=1, num_coin=2)

    def resolve_market(self, player, card):
        self.pluses(player, num_actions=1, num_buys=1, num_coin=1, num_cards=1)

    def resolve_witch(self, player, card):
        self.pluses(player, num_cards=2)
        self.for_each_other_player(player,
                                   self.gain_a_curse)

    def resolve_throne_room(self, player, card):
        self.add_step(player,
                      self.select_throne_room_card)

    def resolve_moneylender(self, player, card):
        copper = self.find_in_hand(player, lambda x: x.name == "Copper")
        if copper is None :
            return

        # Otherwise we trash
        player.hand.remove_card(copper)
        self.trash.push(copper)

        player.money_pool += 3

    def resolve_militia(self, player, card):
        player.money_pool += 2
        self.for_each_other_player(player,
                                   self.discard_down_to_3)

    def resolve_feast(self, player, card):
        self.trash_card(player, card = card, trash_test = self.simple_test)
        self.add_step(player,
                      self.gain,
                      kwargs = {'gain_test': self.costs_up_to_x,
                                'max_cost': 5})

    def resolve_remodel(self, player, card):
        if player.hand.get_num_cards() == 0:
            return
        self.add_step(player,
                      self.trash_cards,
                      kwargs = {'max_cards': 1,
                                'min_cards': 1},
                      save_result_as = 'other_card')
        self.add_step(player,
                      self.gain,
                      kwargs = {'gain_test': self.costs_up_to_x_more,
                                'max_delta': 2})

    def resolve_mine(self, player, card):

        def treasure_and_cost(player, card, other_card, **kwargs):
            if (self.card_type_contians(player, card, "treasure", **kwargs) and
                self.costs_up_to_x_more(player, card, other_card, 3)):
                return True
            return False

        if player.hand.get_num_cards() == 0:
            return

        self.add_step(player,
                      self.trash_cards,
                      kwargs = {'max_cards': 1,
                                'min_cards': 1,
                                'test': self.card_type_contians,
                                'card_type': 'treasure'},
                      save_result_as = 'other_card')
        self.add_step(player,
                      self.gain,
                      kwargs = {'gain_test': treasure_and_cost})

    # TODO: Clean up everything below this.

    def resolve_adventurer(self, player, card):
        set_asside = []
        treasure_cards = []
        while len(treasure_cards) < 2:
            card = self.get_next_card(player)
            if card is None:
                break
            card.face_up = True
            if "treasure" in card.card_type:
                treasure_cards.append(card)
            else:
                set_asside.append(card)
        for card in treasure_cards:
            player.hand.add_card(card)
            card.face_up = False
            card.set_value("face_up", True, player)
        for card in set_asside:
            player.discard.add_card(card)

    def resolve_spy(self, player, card):
        self.draw(player)
        player.num_actions += 1
        for other_player in self.players:
            # Reveal the top card of the deck
            revealed_card = self.get_next_card(other_player)
            if revealed_card is None:
                continue

            revealed_card.face_up = True
            revealed_card.set_value("face_up", True, other_player)
            other_player.play_zone.push(revealed_card)
            self.add_step(player,
                          self.spy_step,
                          kwargs = {'other_player': other_player,
                                    'revealed_card': revealed_card})


    def resolve_library(self, player, card):
        if player.hand.get_num_cards() >= 7:
            return

        while player.hand.get_num_cards() < 7:
            next_card = self.get_next_card(player)
            if next_card is None:
                return
            player.hand.push(next_card)
            next_card.set_value("face_up", True, player)
            if "action" in next_card.card_type:
                # If it's an action we call this again and wait for the user
                # to pass in a value
                self.add_step(player,
                              self.library_step,
                              kwargs = {"next_card": next_card})
                return

    def resolve_bureaucrat(self, player, card):
        def has_victory_card(player):
            for card in player.hand.get_cards():
                if "victory" in card.card_type:
                    return True
            return False

        # Gain a silver
        if self.treasure1.get_num_cards() > 0:
            player.deck.push(self.treasure1.pop())

        for other_player in self.players:
            if other_player != player:
                if has_victory_card(other_player):
                    self.add_step(other_player,
                                  self.put_back_victory_card)

    def resolve_thief(self, player, card):
        for other_player in self.players:
            if other_player != player:
                card1 = self.get_next_card(other_player)
                card2 = self.get_next_card(other_player)

                if card1 is not None:
                    card1.face_up = True
                    card1.set_value("face_up", True, player)
                if card2 is not None:
                    card2.face_up = True
                    card2.set_value("face_up", True, player)

                if ("treasure" in card1.card_type or
                    "treasure" in card2.card_type):

                    other_player.play_zone.push(card1)
                    other_player.play_zone.push(card2)
                    self.add_step(player,
                                  self.thief_trash,
                                  kwargs={"possible_cards": [card1, card2]})
                    self.add_step(player,
                                  self.thief_steal)
                else:
                    other_player.discard.push(card1)
                    other_player.discard.push(card2)
