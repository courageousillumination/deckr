"""
This module contains all test for the Game class.
"""

from unittest import TestCase

from engine.card import Card
from engine.zone import Zone
from engine.player import Player
from engine.game import InvalidMoveException
from engine.tests.mock_game.mock_game import MockGame


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

    def test_set_up(self):
        """
        Make sure that setup can't be called twice
        and that it was run on class creation.
        """

        self.assertTrue(self.game.is_setup)
        self.assertFalse(self.game.set_up())
        self.assertTrue(self.game.is_setup)

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
        self.assertEqual([], self.game.make_action("restricted_action",
                                                   player_id=self.player.game_id))

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

        # The game should know about its zones
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
            'cards': [{'game_id': 1, 'zone': 2},
                      {'game_id': 2, 'zone': 1},
                      {'game_id': 3, 'zone': 1}],
            'players': [{'game_id': 1}],
            'zones': [{'cards': [2, 3],
                       'game_id': 1,
                       'name': 'zone2',
                       'region_id': None,
                       'stacked': True,
                       'zone_type': ''},
                      {'cards': [1],
                       'game_id': 2,
                       'name': 'zone1',
                       'region_id': None,
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
