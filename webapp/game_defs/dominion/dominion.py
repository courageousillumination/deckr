
"""
This module provides an implementation of a game of Dominion
"""

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

    def set_up(self):
        import random

        # Select 10 random kindom cards
        all_kingdom_cards = [x["name"] for x in self.card_set.all_cards() if
                             x["kingdom_card"]]
        kingdom_cards = random.sample(all_kingdom_cards, 10)
        kingdom_cards[0] = "Chapel"
        for i in range(10):
            cards = self.card_set.create(kingdom_cards[i], 10)
            turn_face_up(cards)
            self.zones["kingdom" + str(i)].set_cards(cards)
            self.register(cards)

        # Create treasures, victory and curses.
        cards_to_zones = [('Curse', 'curses', max((len(self.players) - 1)* 10, 0)),
                          ('Estate', 'victory0', 12),
                          ('Duchy', 'victory1', 12),
                          ('Province', 'victory2', 12),
                          ('Copper', 'treasure0', 60 - 7 * len(self.players)),
                          ('Silver', 'treasure1', 40),
                          ('Gold', 'treasure2', 30),
                          ]

        for card, zone, num in cards_to_zones:
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
            self.clean_up(player)

        self.current_phase = "action"
        self.current_player = self.players[0]

    def is_over(self):
        """
        Dominion is over if the provinces are out or three supply piles are
        out.
        """

        if self.victory2.get_num_cards() == 0:
            return True

        #if len([self.zones["kingdom" + i] for i in range(0, 10) if
        #        self.zones["kindgom" + i].get_num_cards() == 0]) >= 3:
        #    return True
        return False


    def winners(self):
        """
        Count up victory points for each player
        """

        def player_score(player):
            score = 0
            for card in (player.hand.get_cards() +
                         player.discard.get_cards() +
                         player.deck.get_cards()):
                if ("victory" in card.card_type or
                   "curse" in card.card_type):
                    score += card.victory_points
            return score

        max_score = float("-inf")
        max_player = None
        for player in self.players:
            score = player_score(player)
            if score > max_score:
                max_score = score
                max_player = [player]
            elif score == max_score:
                max_player.append(player)

        return max_player

    def get_next_card(self, player):
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

    def draw(self, player):
        card = self.get_next_card(player)
        if card is None:
            return
        card.set_value("face_up", True, player)
        player.hand.push(card)

    def action_restrictions(self, player, card):
        if self.current_player != player:
            return False

        # You can only play actions during the action phase
        if self.current_phase == "action":
            if "action" not in card.card_type:
                return False
            # Can't play an action if you don't have any actions...
            if player.num_actions <= 0:
                return False

        # We can only play treasures during the buy stage
        if self.current_phase == "buy" and "treasure" not in card.card_type:
            return False

        return True

    def buy_restrictions(self, player, buy_zone):

        if self.current_player != player:
            return False

        # Make sure that there are cards in that zone
        if buy_zone.get_num_cards() == 0:
            return False

        # TODO: Make sure it's actually a supply pile

        # Make sure we have a buy
        if player.num_buys <= 0:
            return False

        # Make sure we have enough money
        if player.money_pool < buy_zone.peek().cost:
            return False

        return True

    @action(restriction = action_restrictions)
    def play_card(self, player, card):
        player.hand.remove_card(card)
        player.play_zone.add_card(card)

        card.face_up = True
        if "action" in card.card_type:
            player.num_actions -= 1

        self.resolve(player, card)

    @action(restriction = buy_restrictions)
    def buy(self, player, buy_zone):
        card = buy_zone.pop()
        player.discard.push(card)
        player.num_buys -= 1
        player.money_pool -= card.cost

    @action(restriction = None)
    def next_phase(self, player):
        if self.current_phase == "action":
            self.current_phase = "buy"
        elif self.current_phase == "buy":
            self.clean_up(player)
            self.current_phase = "action"
            self.current_player = self.next_player(self.current_player)

    def clean_up(self, player):
        # Move everything from the play zone
        while player.play_zone.get_num_cards() > 0:
            player.discard.push(player.play_zone.pop())

        # Move everything from the hand
        while player.hand.get_num_cards() > 0:
            card = player.hand.pop()
            card.face_up = True
            player.discard.push(card)

        # Draw 5 more
        for _ in range(5):
            self.draw(player)

        # Reset all variables
        player.money_pool = 0
        player.num_actions = 1
        player.num_buys = 1

    def next_player(self, player):
        player_index = self.players.index(player)
        print self.players
        print player_index
        if player_index == (len(self.players) - 1):
            return self.players[0]
        else:
            return self.players[player_index + 1]

    def resolve(self, player, card):
        """
        I need a better way of doing this.
        """

        getattr(self, "resolve_"+card.name.lower())(player, card)


    def cards_in_hand(self, player, cards, min_cards, max_cards, **kwargs):
        if not isinstance(cards, list):
            return False

        if (min_cards is not None and len(cards) < min_cards or
            max_cards is not None and len(cards) > max_cards):
            return False

        for card in cards:
            if card not in player.hand:
                return False

        return True

    # pylint: disable=unused-argument
    @game_step(requires=[("cards", "Cards", cards_in_hand)])
    def discard_cards(self, player, cards, **kwargs):
        """
        Discard the cards in cards, and returns the
        number of cards discarded.
        """

        for card in cards:
            player.hand.remove_card(card)
            player.discard.add_card(card)
            card.face_up = True
        return len(cards)

    @game_step(requires=[("cards", "Cards", cards_in_hand)])
    def trash_cards(self, player, cards, **kwargs):
        """
        Trash a list of cards.
        """

        for card in cards:
            player.hand.remove_card(card)
            self.trash.add_card(card)
            card.face_up = True
        return cards

    @game_step(requires=None)
    def draw_cards(self, player, num_cards, **kwargs):
        for _ in range(num_cards):
            self.draw(player)
        return num_cards

    @game_step(requires=[("flag", "Bool",
                          lambda self, player, flag, **kwargs: True)])
    def discard_deck(self, player, flag, **kwargs):
        pass

    def gain_test_wrapper(self, player, gain_from_zone, gain_test, **kwargs):
        # We can only gain a card if it's there
        if gain_from_zone.get_num_cards == 0:
            return False

        return gain_test(player, gain_from_zone, **kwargs)

    @game_step(requires=[("gain_from_zone", "Zone", gain_test_wrapper)])
    def gain(self, player, gain_from_zone, gain_test, **kwargs):
        # Assumes that the requires check everything is solid in the \
        # gain_from_zone
        card = gain_from_zone.pop()
        player.discard.push(card)

    # All card resolutions go here
    def resolve_copper(self, player, card):
        player.money_pool += 1

    def resolve_silver(self, player, card):
        player.money_pool += 2

    def resolve_gold(self, player, card):
        player.money_pool += 3

    def resolve_moat(self, player, card):
        self.draw(player)
        self.draw(player)

    def resolve_chapel(self, player, card):
        self.add_step(player,
                      self.trash_cards,
                      kwargs = {'max_cards': 4,
                                'min_cards': None})

    def resolve_cellar(self, player, card):
        player.num_actions += 1
        self.add_step(player,
                      self.discard_cards,
                      save_result_as = "num_cards",
                      kwargs = {'min_cards': None,
                                'max_cards': None})
        self.add_step(player, self.draw_cards)

    def resolve_chancellor(self, player, card):
        player.money_pool += 2
        self.add_step(self.discard_deck)

    def resolve_village(self, player, card):
        player.num_actions += 2
        self.draw(player)

    def resolve_woodcutter(self, player, card):
        player.num_buys += 1
        player.money_pool += 2

    def resolve_workshop(self, player, card):
        def costs_up_to_4(player, gain_from_zone, **kwargs):
            return gain_from_zone.peek().cost <= 4
        self.add_step(player,
                      self.gain,
                      kwargs = {'gain_test': costs_up_to_4})

    def resolve_smithy(self, player, card):
        self.draw(player)
        self.draw(player)
        self.draw(player)

    def resolve_council_room(self, player, card):
        self.draw(player)
        self.draw(player)
        self.draw(player)
        self.draw(player)

        player.num_buys += 1

        for other_player in self.players:
            if other_player != player:
                self.draw(other_player)

    def resolve_laboratory(self, player, card):
        self.draw(player)
        self.draw(player)
        player.num_actions += 1

    def resolve_festival(self, player, card):
        player.num_actions += 2
        player.num_buys += 1
        player.money_pool += 2

    def resolve_market(self, player, card):
        self.draw(player)
        player.num_actions += 1
        player.num_buys += 1
        player.money_pool += 1

    def resolve_witch(self, player, card):
        self.draw(player)
        self.draw(player)

        for other_player in self.players:
            if other_player != player:
                pass
                #self.draw(other_player)

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

    def resolve_feast(self, player, card):
        card.zone.remove_card(card)
        self.trash.push(card)

        def costs_up_to_5(player, gain_from_zone, **kwargs):
            return gain_from_zone.peek().cost <= 5
        self.add_step(player,
                      self.gain,
                      kwargs = {'gain_test': costs_up_to_5})

    def resolve_militia(self, player, card):
        pass

    def resolve_moneylender(self, player, card):
        coppers = [x for x in player.hand.get_cards() if x.name == "Copper"]
        if len(coppers == 0):
            return

        # Trash one of them
        copper = coppers[0]
        player.hand.remove_card(copper)
        player.money_pool += 3
        self.trash.push(copper)

    def resolve_remodel(self, player, card):
        if player.hand.get_num_cards() == 0:
            return

        self.add_step(player,
                      self.trash_cards,
                      kwargs = {'max_cards': 1,
                                'min_cards': 1},
                      save_result_as = 'trashed_card')
        def costs_up_to_2_more(player, gain_from_zone, trashed_card, **kwargs):
            return trashed_card[0].cost + 2 >= gain_from_zone.peek().cost

        self.add_step(player,
                      self.gain,
                      kwargs = {'gain_test': costs_up_to_2_more})

    def resolve_spy(self, player, card):
        pass

    def resolve_thief(self, player, card):
        pass

    def resolve_throne_room(self, player, card):
        pass

    def resolve_library(self, player, card):
        pass
