"""
This module contains all test for the Game class.
"""

from unittest import skip, TestCase

from engine.card import Card
from engine.game import game_step, InvalidMoveException, NeedsMoreInfo, action
from engine.player import Player
from engine.tests.mock_game.mock_game import MockGame
from engine.zone import Zone


class GameTestCase(TestCase):

    """
    A simple test case for our game class. Note that this
    also tests the only functionality that we care about
    for the Card and Zone classes since these are mostly
    data containers and don't contain any functionality.
    """

    def setUp(self):
        self.game = MockGame()
        self.game.set_up()
        self.player = Player()
        self.game.register([self.player])
        self.game.players = [self.player]

    def test_set_up(self):
        """
        Make sure that setup can't be called twice
        and that it was run on class creation.
        """

        self.assertTrue(self.game.is_setup)
        self.assertFalse(self.game.set_up())
        self.assertTrue(self.game.is_setup)

    def test_action(self):
        """
        Make sure that action restrictions work correctly
        """

        def restriction_pass(*args, ** kwargs):
            """
            Always returns true
            """
            return True

        def restriction_fail(*args, ** kwargs):
            """
            Always returns false
            """
            return False

        @action()
        def mock_action1(*args, ** kwargs):
            """
            Should always return 1
            """
            return 1

        @action(restriction=restriction_pass)
        def mock_action2(*args, ** kwargs):
            """
            Should always return 2
            """
            return 2

        @action(restriction=restriction_fail)
        def mock_action3(*args, ** kwargs):
            """
            Should always fail with an InvalidMoveException
            """
            return 3

        self.assertEqual(mock_action1(), 1)
        self.assertEqual(mock_action2(), 2)
        self.assertRaises(InvalidMoveException, mock_action3, "Invalid Move")

    def test_registration(self):
        """
        Make sure that assigning IDs works.
        """

        card1 = Card()
        card2 = Card()

        zone1 = Zone()
        zone2 = Zone()

        self.assertIsNone(card1.game_id)
        self.assertIsNone(card2.game_id)
        self.assertIsNone(zone1.game_id)
        self.assertIsNone(zone2.game_id)

        # Make sure we can assign ids to a set of cards
        self.game.register((card1, card2))

        self.assertEqual(card1.game_id, 1)
        self.assertEqual(card2.game_id, 2)

        # Make sure we can access the objects from the game
        self.assertEqual(self.game.get_object_with_id("Card", 1), card1)
        self.assertEqual(self.game.get_object_with_id("Card", 2), card2)

        # Make sure that we don't change ids if the id
        # is already there.

        self.game.register((card2, card1))

        self.assertEqual(card1.game_id, 1)
        self.assertEqual(card2.game_id, 2)

        # Make sure that we assign different ids to different
        # classes.

        self.game.register((zone1, zone2))

        self.assertEqual(zone1.game_id, 1)
        self.assertEqual(zone2.game_id, 2)

        # Make sure we can access the objects from the game
        self.assertEqual(self.game.get_object_with_id("Zone", 1), zone1)
        self.assertEqual(self.game.get_object_with_id("Zone", 2), zone2)

        # Make sure we know what to do on edge cases
        self.game.register([])

    @skip
    def test_make_action(self):
        """
        Make sure that restrictions work on making actions.
        """

        self.game.phase = "restricted"

        self.assertRaises(InvalidMoveException,
                          self.game.make_action,
                          "restricted_action",
                          player_id=self.player.game_id)
        self.game.phase = "unrestricted"
        player_id = self.player.game_id
        self.game.make_action("restricted_action", player_id=player_id)

        self.assertEqual([('is_over', [1])],
                         self.game.get_public_transitions())

        self.assertRaises(InvalidMoveException,
                          self.game.make_action,
                          "foobar")

    def test_make_action_substitution(self):
        """
        Makes sure that make action actually makes proper substitutions
        depending on variable name.
        """

        card = Card()
        zone = Zone()
        self.game.register([card, zone])

        self.game.make_action('test_argument_types',
                              card=card.game_id,
                              zone=zone.game_id,
                              player=self.player.game_id)

    def test_add_player(self):
        """
        Make sure we can add the propre number of players.
        """

        self.game.max_players = 2
        self.assertEqual(self.game.add_player(), 2)
        self.assertRaises(ValueError, self.game.add_player)

    def test_make_winning_action(self):
        """
        Make sure that we can win the game.
        """

        self.game.make_action("win", player_id=self.player.game_id)
        self.assertTrue(self.game.is_over())
        self.assertListEqual([1], self.game.winners())

    def test_make_losing_action(self):
        """
        Make sure that we can lose the game.
        """

        self.game.make_action("lose", player_id=self.player.game_id)
        self.assertTrue(self.game.is_over())
        self.assertListEqual([], self.game.winners())

    def test_load_config(self):
        """
        Make sure that we can load the configuration of a game.
        """

        config = {
            "max_players": 1,
            "zones": [
                {"name": "zone1"},
                {"name": "zone2", "stacked": True}
            ]
        }

        self.game.load_config(config)

        # The game should know the maximum number of players
        self.assertEqual(self.game.max_players, 1)

        # The game should know about its zones and card definitions
        self.assertEqual(len(self.game.zones), 2)

        # The game should have created actual attributes for
        # each of the zones
        self.assertTrue(hasattr(self.game, "zone1"))
        self.assertTrue(hasattr(self.game, "zone2"))

        # The zones should know about their configuration
        self.assertFalse(self.game.zones["zone1"].stacked)
        self.assertTrue(self.game.zones["zone2"].stacked)

        # Make sure that all zones were given an id
        self.assertIsNotNone(self.game.zones["zone1"].game_id)

    @skip
    def test_load_card_set_config(self):
        """
        This test will try to load a configuration with an embeded card set.
        This should register the card set with the game.
        """

        config = {
            "max_players": 1,
            "card_set": [
                {"name": "card1"},
                {"name": "card2"}
            ]
        }

        self.game.load_config(config)

        self.assertTrue(hasattr(self.game, 'card_set'))
        self.assertEqual(len(self.game.card_set.all_cards()), 2)

    def test_config_with_owners(self):
        """
        Test allowing configurations to specify zone ownership.
        """

        config = {
            "max_players": 3,
            "zones": [
                {"name": "zone1", "owner": "player"},
                {"name": "zone2"}
            ]
        }

        self.game.load_config(config)

        # Game should be aware of its players and zones
        self.assertEqual(self.game.max_players, 3)
        self.assertEqual(len(self.game.zones), 1)

        player1 = self.game.get_object_with_id("Player", self.game.add_player())
        player2 = self.game.get_object_with_id("Player", self.game.add_player())

        # Players should be aware of their assigned zones, and only those zones
        self.assertTrue(hasattr(player1, "zone1"))
        self.assertFalse(hasattr(player1, "zone2"))

        self.assertTrue(hasattr(player2, "zone1"))
        self.assertFalse(hasattr(player2, "zone2"))

        # Players should also have dictionary of their zones
        self.assertEqual(len(player1.zones), 1)
        self.assertEqual(len(player2.zones), 1)

        # The game should be aware of the zones and who has them, if anyone
        self.assertEqual(self.game.zones["zone1_"
                                         + str(player1.game_id)], player1.zone1)
        self.assertEqual(self.game.zones["zone1_"
                                         + str(player2.game_id)], player2.zone1)
        self.assertEqual(self.game.zones["zone2"], self.game.zone2)

    def test_config_multi(self):
        """
        Test allowing configurations to specify zone multiplicity.
        """

        config = {
            "max_players": 3,
            "zones": [
                {"name": "zoneA", "multiplicity": 10},
                {"name": "zoneB", "owner": "player", "multiplicity": 10}
            ]
        }

        self.game.load_config(config)
        player1 = self.game.get_object_with_id("Player", self.game.add_player())

        # First we should have 20 zones, 10 of "zoneA"
        # and 10 "zoneB"s belonging to "player1"
        self.assertEqual(len(self.game.zones), 20)

        for i in range(1, 11):
            # The ownerless zones should simply be numbered in order
            self.assertEqual(self.game.zones["zoneA" + str(i)],
                             getattr(self.game, "zoneA" + str(i)))

            # Player1's zones should be numbered and include game_id
            # "Player" should have attributes for its zones
            self.assertTrue(hasattr(player1, "zoneB" + str(i)))
            self.assertEqual(self.game.zones["zoneB" + str(i)
                                             + "_" + str(player1.game_id)],
                             getattr(player1, "zoneB" + str(i)))

        other_player = self.game.get_object_with_id("Player",
                                                    self.game.add_player())

        # Now there are 30 zones, because "other_player" also has 10 "zoneB"s
        self.assertEqual(len(self.game.zones), 30)

        # New zones should be numbered and tagged with other_player's game_id
        # The player should also be aware of them as attributes
        for i in range(1, 11):
            self.assertTrue(hasattr(other_player, "zoneB" + str(i)))
            self.assertEqual(self.game.zones["zoneB" + str(i) +
                                             "_" + str(other_player.game_id)],
                             getattr(other_player, "zoneB" + str(i)))

        # Check that player dictionaries have the right number of elements
        self.assertEqual(len(player1.zones), 10)
        self.assertEqual(len(other_player.zones), 10)

    def test_load_invalid_config(self):
        """
        This test makes sure we can process a configuration
        dict with unexpected fields (these should just be discarded)
        """

        invalid_configuration = {
            "bad_id": "foo",
            "zones": [
                {"name": "zone1", "invalid_field": True}
            ]
        }

        self.game.load_config(invalid_configuration)

    def test_invalid_owner(self):
        """
        This test makes sure we can process a configuration
        dict with a bad owner field.
        """

        bad_config = {
            "max_players": 2,
            "zones": [
                {"name": "zone1", "owner": "player"},
                {"name": "zone2"},
                {"name": "zone3", "owner": "foo"}
            ]
        }

        self.game.load_config(bad_config)

        other_player = self.game.get_object_with_id("Player",
                                                    self.game.add_player())

        # Game should contain only the valid zones
        self.assertEqual(len(self.game.zones), 2)

        # Game should have attributes for the valid zones
        self.assertTrue(hasattr(self.game, "zone1_"
                                + str(other_player.game_id)))
        self.assertTrue(hasattr(self.game, "zone2"))

        # The player should have one zone
        self.assertTrue(hasattr(other_player, "zone1"))

        # Game should not contain the invalid zone
        self.assertFalse(hasattr(self.game, "zone3"))

    def test_get_state(self):
        """
        Make sure that we can get the state out of a Game.
        """

        config = {
            "max_players": 1,
            "zones": [
                {"name": "zone1"},
                {"name": "zone2", "stacked": True}
            ]
        }

        expected_state = {
            'cards': [{'game_id': 1, 'zone': 2, 'face_up': False},
                      {'game_id': 2, 'zone': 1, 'face_up': False},
                      {'game_id': 3, 'zone': 1, 'face_up': False}],
            'players': [{'game_id': 1}],
            'zones': [{'cards': [2, 3],
                       'game_id': 1,
                       'name': 'zone2',
                       'region_id': None,
                       'owner': None,
                       'stacked': True,
                       'zone_type': ''},
                      {'cards': [1],
                       'game_id': 2,
                       'name': 'zone1',
                       'region_id': None,
                       'owner': None,
                       'stacked': False,
                       'zone_type': ''}]
        }

        self.game.load_config(config)

        card1 = Card()
        card2 = Card()
        card3 = Card()
        cards = [card1, card2, card3]
        self.game.register(cards)

        self.game.zone1.push(card1)
        self.game.zone2.push(card2)
        self.game.zone2.push(card3)

        self.assertDictEqual(self.game.get_state(),
                             expected_state)

    def test_state_with_owners(self):
        """
        This tests getting the state of the game when zones
        assigned to players.
        """

        config = {
            "max_players": 3,
            "zones": [
                {"name": "zone1", "owner": "player"}
            ]
        }

        expected_state = {
            'cards': [],
            'players': [{'game_id': 1}],
            'zones': []
        }

        self.game.load_config(config)
        self.assertDictEqual(self.game.get_state(),
                             expected_state)

        other_player = self.game.add_player()

        expected_state = {
            'cards': [],
            'players': [{'game_id': 1},
                        {'game_id': 2,
                         'zones': {'zone1': 1},
                         'zone1': 1}],
            'zones': [{'cards': [],
                       'game_id': 1,
                       'name': 'zone1',
                       'region_id': None,
                       'owner': other_player,
                       'stacked': False,
                       'zone_type': ''}]
        }

        self.assertDictEqual(self.game.get_state(), expected_state)

    def test_state_with_multiplicity(self):
        """
        This tests getting the state of the game when multiple
        zones are created at once.
        """

        config = {
            "max_players": 2,
            "zones": [
                {"name": "zoneA", "owner": "player", "multiplicity": 2}
            ]
        }

        self.game.load_config(config)
        other_player = self.game.add_player()

        expected_state = {
            'cards': [],
            'players': [{'game_id': 1},
                        {'zones': {'zoneA2': 1,
                                   'zoneA1': 2},
                         'zoneA2': 1,
                         'zoneA1': 2,
                         'game_id': 2}],
            'zones': [{'name': 'zoneA2',
                       'stacked': False,
                       'region_id': None,
                       'cards': [],
                       'owner': other_player,
                       'zone_type': '',
                       'game_id': 1},
                      {'name': 'zoneA1',
                       'stacked': False,
                       'region_id': None,
                       'cards': [],
                       'owner': other_player,
                       'zone_type': '',
                       'game_id': 2}]}

        print other_player
        print self.game.get_state()
        self.assertDictEqual(self.game.get_state(),
                             expected_state)

    @skip
    def test_multi_step_action(self):
        """
        Make sure that all of the actions on a card get resolved when it is
        played. This test will call an action that has three steps. The first
        one should run, and then the second one needs input so it should stop.
        When we send it more information then we should see the rest of the
        steps execute.
        """

        self.game.make_action("test_multi_step")
        self.assertListEqual([("step1",)],
                             self.game.get_transitions())

        self.game.flush_transitions()
        # Now we send the additional information
        self.game.make_action("send_information", num=6)
        self.assertListEqual([("step2", 6),
                              ("step3", 6)],
                             self.game.get_transitions())

    @skip
    def test_expected_action(self):
        """
        Make sure that we can query the game to see what it thinks
        the next action should be.
        """

        self.assertIsNone(self.game.get_expected_action())

        # Now if we make a multistep action we should expect send_information
        self.game.make_action("test_multi_step")
        self.assertEqual(self.game.get_expected_action(),
                         ("send_information", "num"))

    @skip
    def test_add_step(self):
        """
        Test to see if we can add a step and run it.
        """

        @game_step(requires=None)
        def simple_step(self):
            """ Adds a simple transition to the game."""
            self.add_transition(("simple_step",))

        self.game.add_step(simple_step)
        self.game.run()
        self.assertListEqual([("simple_step",)],
                             self.game.get_transitions())

    @skip
    def test_game_step_decorator(self):
        """
        Test that the game_Step decorator does what we expect it to (run if
        it has the right arguments or throw an exception otherwise).
        """

        @game_step(requires="num")
        def simple_step(num):
            """ Returns the input. """
            return num

        self.assertRaises(NeedsMoreInfo, simple_step)
        self.assertEqual(simple_step(num=10), 10)

    @skip
    def test_add_transition(self):
        """
        Make sure that we can add transitions, both publicly and on a per player
        basis.
        """

        self.game.add_transition(("foo", "bar"))
        self.game.add_transition(("baz",), self.player)

        self.assertListEqual([("foo", "bar")],
                             self.game.get_public_transitions())
        transitions = self.game.get_player_transitions(self.player.game_id)
        self.assertListEqual([("baz",)], transitions)

    @skip
    def test_remove_player(self):
        """
        Make sure players can be removed by player_id
        """
        player = self.game.players[0].game_id
        self.assertTrue(self.game.remove_player(player))
        self.assertFalse(self.game.remove_player(player))
        self.game.max_players = 3
        newplayer = self.game.add_player()
        newplayertwo = self.game.add_player()
        self.assertTrue(self.game.remove_player(newplayer))
        self.assertFalse(self.game.remove_player(newplayer))
        self.assertTrue(self.game.remove_player(newplayertwo))
