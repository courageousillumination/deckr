from unittest import TestCase

from engine.game_runner import load_game_definition


class DominionTestCase(TestCase):

    def setUp(self):
        self.game, config = load_game_definition("game_defs/dominion")
        self.game.load_config(config)
        self.player1 = self.game.get_object_with_id("Player",
                                                    self.game.add_player())
        self.player2 = self.game.get_object_with_id("Player",
                                                    self.game.add_player())
        self.game.phase = "action"
        self.game.current_player = self.player1
        self.player1.num_actions = 1
        self.player1.num_buys = 1
        self.player1.money_pool = 0

        self.player2.num_actions = 1
        self.player2.num_buys = 1
        self.player2.money_pool = 0

    def create_cards(self, card_name, num = 1):
        cards = self.game.card_set.create(card_name, num)
        if num  == 1:
            self.game.register([cards])
        else:
            self.game.register(cards)
        return cards

    def test_set_up(self):
        self.game.set_up()

        # Make sure each player has 5 cards in the hand and deck
        self.assertEqual(self.player1.hand.get_num_cards(), 5)
        self.assertEqual(self.player1.deck.get_num_cards(), 5)

    def test_cellar(self):
        cellars = self.create_cards("Cellar", 5)
        coppers = self.create_cards("Copper", 4)
        self.player1.hand.set_cards(cellars)
        self.player1.deck.set_cards(coppers)

        self.game.make_action("play_card", player=self.player1.game_id,
                              card=cellars.pop().game_id)
        # Make sure we're expecting some information back
        self.assertEqual(self.game.get_expected_action(),
                         ('send_information', 'cards',
                          'Cards', self.player1.game_id))
        # Make sure when we send the information the cards get discarded
        self.game.make_action("send_information", player=self.player1.game_id,
                              cards=[x.game_id for x in cellars])

        self.assertEqual(self.player1.hand.get_num_cards(), 4)
        self.assertEqual(self.player1.deck.get_num_cards(), 0)
        for copper in coppers:
            self.assertIn(copper, self.player1.hand)


    def test_chapel(self):
        """
        The chapel should allow you to trash up to four cards.
        """

        chapel = self.create_cards("Chapel")
        coppers = self.create_cards("Copper", 4)
        self.player1.hand.set_cards(coppers)
        self.player1.hand.push(chapel)

        self.game.make_action("play_card", player=self.player1.game_id,
                              card=chapel.game_id)
        # Make sure we're expecting some information back
        self.assertEqual(self.game.get_expected_action(),
                         ('send_information', 'cards',
                          'Cards', self.player1.game_id))
        self.game.make_action("send_information", player=self.player1.game_id,
                              cards=[x.game_id for x in coppers])

        self.assertEqual(self.player1.hand.get_num_cards(), 0)
        self.assertEqual(self.game.trash.get_num_cards(), 4)
        for copper in coppers:
            self.assertIn(copper, self.game.trash)

    def test_moat(self):
        """
        The moat shoud allow you to draw two extra cards.
        """

        moat = self.create_cards("Moat")
        coppers = self.create_cards("Copper", 2)
        self.player1.hand.push(moat)
        self.player1.deck.set_cards(coppers)
        self.game.make_action("play_card", player=self.player1.game_id,
                              card=moat.game_id)

        self.assertEqual(self.player1.hand.get_num_cards(), 2)
        self.assertEqual(self.player1.deck.get_num_cards(), 0)

    def test_village(self):
        """
        The village should give +1 card, +2 actions
        """

        village = self.create_cards("Village")
        coppers = self.create_cards("Copper", 2)
        self.player1.hand.push(village)
        self.player1.deck.set_cards(coppers)
        self.game.make_action("play_card", player=self.player1.game_id,
                              card=village.game_id)

        self.assertEqual(self.player1.hand.get_num_cards(), 1)
        self.assertEqual(self.player1.deck.get_num_cards(), 1)
        self.assertEqual(self.player1.num_actions, 2)

    def test_chancellor(self):
        """
        The chancellor should give +2 coin and allow you to
        discard your deck.
        """

        chancellor = self.create_cards("Chancellor")
        coppers = self.create_cards("Copper", 2)
        self.player1.hand.push(chancellor)
        self.player1.deck.set_cards(coppers)
        self.game.make_action("play_card", player=self.player1.game_id,
                              card=chancellor.game_id)

        self.assertEqual(self.game.get_expected_action(),
                         ('send_information', 'flag',
                          'Bool', self.player1.game_id))
        # Make sure when we send the information the cards get discarded
        self.game.make_action("send_information", player=self.player1.game_id,
                              flag=True)

        self.assertEqual(self.player1.hand.get_num_cards(), 0)
        self.assertEqual(self.player1.deck.get_num_cards(), 0)
        self.assertEqual(self.player1.discard.get_num_cards(), 2)
        self.assertEqual(self.player1.money_pool, 2)

    def test_woodcutter(self):
        """
        The village should give +1 card, +2 actions
        """

        woodcutter = self.create_cards("Woodcutter")
        self.player1.hand.push(woodcutter)
        self.game.make_action("play_card", player=self.player1.game_id,
                              card=woodcutter.game_id)


        self.assertEqual(self.player1.money_pool, 2)
        self.assertEqual(self.player1.num_buys, 2)

    def test_workshop(self):
        """
        The workshop should allow you to gain a card costing
        up to 4.
        """

        workshop = self.create_cards("Workshop")
        silver = self.create_cards("Silver")
        self.player1.hand.push(workshop)
        self.game.treasure0.push(silver)

        self.game.make_action("play_card", player=self.player1.game_id,
                              card=workshop.game_id)

        self.assertEqual(self.game.get_expected_action(),
                         ('send_information', 'gain_from_zone',
                          'Zone', self.player1.game_id))
        self.game.make_action("send_information", player=self.player1.game_id,
                              gain_from_zone=self.game.treasure0.game_id)

        self.assertEqual(self.game.treasure0.get_num_cards(), 0)
        self.assertIn(silver, self.player1.discard)

    def test_bureaucrat(self):
        """
        The Bureaucrat should give you a silver on top of your deck and
        force each other player to put back a victory card.
        """

        bureaucrat = self.create_cards("Bureaucrat")
        silver = self.create_cards("Silver")
        estate = self.create_cards("Estate")
        self.player1.hand.push(bureaucrat)
        self.player2.hand.push(estate)
        self.game.treasure1.push(silver)

        self.game.make_action("play_card", player=self.player1.game_id,
                              card=bureaucrat.game_id)

        self.assertEqual(self.game.get_expected_action(),
                         ('send_information', 'card',
                          'Card', self.player2.game_id))
        self.game.make_action("send_information", player=self.player1.game_id,
                              card=estate.game_id)

        self.assertEqual(self.game.treasure1.get_num_cards(), 0)
        self.assertIn(silver, self.player1.deck)
        self.assertIn(estate, self.player2.deck)

    def test_feast(self):
        """
        The feast should allow you to trash it and gain a card costing up
        to 5.
        """

        feast = self.create_cards("Feast")
        market = self.create_cards("Market")
        self.player1.hand.push(feast)
        self.game.kingdom0.push(market)

        self.game.make_action("play_card", player=self.player1.game_id,
                              card=feast.game_id)

        self.assertEqual(self.game.get_expected_action(),
                         ('send_information', 'gain_from_zone',
                          'Zone', self.player1.game_id))
        self.game.make_action("send_information", player=self.player1.game_id,
                              gain_from_zone=self.game.kingdom0.game_id)

        self.assertEqual(self.game.kingdom0.get_num_cards(), 0)
        self.assertIn(market, self.player1.discard)

    def test_gardens(self):
        """
        The garden should be worth one point for every 10 cards in your deck.
        """

        garden = self.create_cards("Gardens")
        coppers = self.create_cards("Copper", 19)
        estate = self.create_cards("Estate")
        self.player1.deck.set_cards(coppers)
        self.player1.hand.add_card(garden)
        self.player2.hand.add_card(estate)

        self.assertEqual(self.game.winners(), [self.player1])

    def test_militia(self):
        """
        The militia should give 2 coin and force everyone else to discard down
        to 3 cards.
        """

        militia = self.create_cards("Militia")
        coppers = self.create_cards("Copper", 5)
        self.player1.hand.push(militia)
        self.player2.hand.set_cards(coppers)

        self.game.make_action("play_card", player=self.player1.game_id,
                              card=militia.game_id)

        self.assertEqual(self.game.get_expected_action(),
                         ('send_information', 'cards',
                          'Cards', self.player2.game_id))
        self.game.make_action("send_information", player=self.player2.game_id,
                              cards=[coppers[0].game_id, coppers[1].game_id])

        self.assertEqual(self.player2.hand.get_num_cards(), 3)
        self.assertEqual(self.player2.discard.get_num_cards(), 2)
        self.assertEqual(self.player1.money_pool, 2)

    def test_moneylender(self):
        """
        The moneylender should allow you to trash a copper and gain
        +$3
        """

        copper = self.create_cards("Copper")
        moneylender = self.create_cards("Moneylender")
        self.player1.hand.push(moneylender)
        self.player1.hand.push(copper)

        self.game.make_action("play_card", player=self.player1.game_id,
                              card=moneylender.game_id)

        self.assertEqual(self.player1.hand.get_num_cards(), 0)
        self.assertEqual(self.game.trash.get_num_cards(), 1)
        self.assertEqual(self.player1.money_pool, 3)

    def test_remodel(self):
        """
        Should allow you to trash a card and gain one costing up to 4 more.
        """

        copper = self.create_cards("Copper")
        moat = self.create_cards("Moat")
        remodel = self.create_cards("Remodel")
        self.player1.hand.push(remodel)
        self.player1.hand.push(copper)
        self.game.kingdom0.push(moat)

        self.game.make_action("play_card", player=self.player1.game_id,
                              card=remodel.game_id)

        self.assertEqual(self.game.get_expected_action(),
                         ('send_information', 'card',
                          'Card', self.player1.game_id))
        self.game.make_action("send_information", player=self.player1.game_id,
                              card = copper.game_id)

        self.assertEqual(self.game.get_expected_action(),
                         ('send_information', 'gain_from_zone',
                          'Zone', self.player1.game_id))
        self.game.make_action("send_information", player=self.player1.game_id,
                              gain_from_zone = self.game.kingdom0.game_id)

        self.assertEqual(self.player1.hand.get_num_cards(), 0)
        self.assertEqual(self.game.trash.get_num_cards(), 1)
        self.assertIn(moat, self.player1.discard)

    def test_smithy(self):
        """
        The smithy should give +3 cards
        """

        smithy = self.create_cards("Smithy")
        coppers = self.create_cards("Copper", 3)
        self.player1.hand.push(smithy)
        self.player1.deck.set_cards(coppers)
        self.game.make_action("play_card", player=self.player1.game_id,
                              card=smithy.game_id)

        self.assertEqual(self.player1.hand.get_num_cards(), 3)
        self.assertEqual(self.player1.deck.get_num_cards(), 0)

    def test_spy(self):
        """
        The spy should give +1 card, +1 action and then reveal each card
        and you get to choose to discard it or not.
        """

        spy = self.create_cards("Spy")
        player_1_copper = self.create_cards("Copper", 2)
        player_2_copper = self.create_cards("Copper")

        self.player1.hand.push(spy)
        self.player1.deck.set_cards(player_1_copper)
        self.player2.deck.push(player_2_copper)

        self.game.make_action("play_card", player=self.player1.game_id,
                              card=spy.game_id)

        # Keep our copper, and force player2 to discard his
        self.game.make_action("send_information", player=self.player1.game_id,
                              discard = False)
        self.game.make_action("send_information", player=self.player1.game_id,
                              discard = True)

        self.assertEqual(self.player1.hand.get_num_cards(), 1)
        self.assertEqual(self.player1.num_actions, 1)
        self.assertIn(player_1_copper[1], self.player1.hand)
        self.assertIn(player_1_copper[0], self.player1.deck)
        self.assertIn(player_2_copper, self.player2.discard)


    def test_thief(self):
        """
        The thief should reveal the top 2 cards, you can trash a treasure, and
        then have the choice of gaining a treasure.
        """

        thief = self.create_cards("Thief")
        coppers = self.create_cards("Copper", 2)

        self.player1.hand.push(thief)
        self.player2.deck.set_cards(coppers)

        self.game.make_action("play_card", player=self.player1.game_id,
                              card=thief.game_id)

        # Keep our copper, and force player2 to discard his
        self.game.make_action("send_information", player=self.player1.game_id,
                              card = coppers[0].game_id)
        self.game.make_action("send_information", player=self.player1.game_id,
                              steal = True)


        self.assertIn(coppers[0], self.player1.discard)
        self.assertIn(coppers[1], self.player2.discard)

    def test_throne_room(self):
        """
        The throneroom should allow you to play an action twice.
        """

        throne_room = self.create_cards("Throne Room")
        smithy = self.create_cards("Smithy")
        coppers = self.create_cards("Copper", 6)
        self.player1.hand.push(throne_room)
        self.player1.hand.push(smithy)
        self.player1.deck.set_cards(coppers)

        self.game.make_action("play_card", player=self.player1.game_id,
                              card=throne_room.game_id)
        self.game.make_action("send_information", player=self.player1.game_id,
                              card = smithy.game_id)

        self.assertEqual(self.player1.hand.get_num_cards(), 6)
        self.assertEqual(self.player1.deck.get_num_cards(), 0)


    def test_council_room(self):
        """
        The council room should give +4 cards, +1 buy, and each other player
        draws a card.
        """

        council_room = self.create_cards("Council Room")
        coppers = self.create_cards("Copper", 4)
        other_coppers = self.create_cards("Copper")
        self.player1.hand.push(council_room)
        self.player1.deck.set_cards(coppers)
        self.player2.deck.push(other_coppers)
        self.game.make_action("play_card", player=self.player1.game_id,
                              card=council_room.game_id)

        self.assertEqual(self.player1.hand.get_num_cards(), 4)
        self.assertEqual(self.player1.num_buys, 2)
        self.assertEqual(self.player2.hand.get_num_cards(), 1)

    def test_festival(self):
        """
        The festival shoud give +2 actions, + 1 buy, + $2
        """

        festival = self.create_cards("Festival")
        self.player1.hand.push(festival)
        self.game.make_action("play_card", player=self.player1.game_id,
                              card=festival.game_id)

        self.assertEqual(self.player1.num_buys, 2)
        self.assertEqual(self.player1.num_actions, 2)
        self.assertEqual(self.player1.money_pool, 2)

    def test_laboratory(self):
        """
        The lab should give +2 cards, +1 action.
        """

        lab = self.create_cards("Laboratory")
        coppers = self.create_cards("Copper", 2)
        self.player1.hand.push(lab)
        self.player1.deck.set_cards(coppers)
        self.game.make_action("play_card", player=self.player1.game_id,
                              card=lab.game_id)

        self.assertEqual(self.player1.hand.get_num_cards(), 2)
        self.assertEqual(self.player1.num_actions, 1)

    def test_library(self):
        """
        The library should draw up to 7 cards, putting aside actions.
        """

        pass

    def test_market(self):
        """
        The market should give +1 card; +1 action; +1 buy; +$1
        """

        market = self.create_cards("Market")
        coppers = self.create_cards("Copper")
        self.player1.hand.push(market)
        self.player1.deck.push(coppers)
        self.game.make_action("play_card", player=self.player1.game_id,
                              card=market.game_id)

        self.assertEqual(self.player1.hand.get_num_cards(), 1)
        self.assertEqual(self.player1.num_buys, 2)
        self.assertEqual(self.player1.num_actions, 1)
        self.assertEqual(self.player1.money_pool, 1)

    def test_mine(self):
        """
        The mine should allow you to trash a treasure card and get one
        costing up to 3 more.
        """

        pass

    def test_witch(self):
        """
        The witch should give +2 cards and give each other player a  curse.
        """

        witch = self.create_cards("Witch")
        coppers = self.create_cards("Copper", 2)
        curse = self.create_cards("Curse")

        self.player1.hand.push(witch)
        self.player1.deck.set_cards(coppers)
        self.game.curses.push(curse)

        self.game.make_action("play_card", player=self.player1.game_id,
                              card=witch.game_id)

        self.assertEqual(self.player1.hand.get_num_cards(), 2)
        self.assertIn(curse, self.player2.discard)

    def test_adventurer(self):
        """
        The adventurer should dig for two treasure cards in your deck and
        discard the rest.
        """

        pass
