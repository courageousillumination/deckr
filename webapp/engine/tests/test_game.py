"""
This module contains all test for the Game class.
"""

from unittest import skip, TestCase

from engine.card import Card
from engine.game import InvalidMoveException
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
            "cards": [
                {"name": "card1"},
                {"name": "card2", "type": "Instant", "effect": "destroy cards"}
            ]
        }

        self.game.load_config(config)

        # The game should know the maximum number of players
        self.assertEqual(self.game.max_players, 1)

        # The game should know about its zones and card definitions
        self.assertEqual(len(self.game.zones), 2)
        self.assertEqual(len(self.game.card_defs), 2)

        # The game should have created actual attributes for
        # each of the zones
        self.assertTrue(hasattr(self.game, "zone1"))
        self.assertTrue(hasattr(self.game, "zone2"))

        # The game should have created actual attributes for
        # each of the card definitions
        self.assertTrue(hasattr(self.game, "card1"))
        self.assertTrue(hasattr(self.game, "card2"))

        # The zones should know about their configuration
        self.assertFalse(self.game.zones["zone1"].stacked)
        self.assertTrue(self.game.zones["zone2"].stacked)

        # The cards should know about their attributes
        self.assertEqual(self.game.card_defs["card2"].type, "Instant")
        self.assertEqual(self.game.card_defs["card2"].effect, "destroy cards")

        # Make sure that all zones were given an id
        self.assertIsNotNone(self.game.zones["zone1"].game_id)

    @skip("not yet implemented")
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
        self.assertEqual(len(self.game.zones), 2)

        player1 = self.game.add_player()
        player2 = self.game.add_player()

        # Players should be aware of their assigned zones, and only those zones
        self.assertTrue(hasattr(player1, "zone1"))
        self.assertFalse(hasattr(player1, "zone2"))

        self.assertTrue(hasattr(player2, "zone1"))
        self.assertFalse(hasattr(player2, "zone2"))

        # The game should be aware of the zones and who has them, if anyone
        self.assertEqual(self.games.zones["zone1_" +
                                          str(self.game.player1.game_id)], player1.zone1)
        self.assertEqual(self.games.zones["zone1_" +
                                          str(self.game.player2.game_id)], player2.zone1)
        self.assertEqual(self.games.zones["zone2"], self.game.zone2)

    @skip("not yet implemented")
    def test_config_multi(self):
        """
        Test allowing configurations to specify zone multiplicity.
        """

        config = {
            "max_players": 2,
            "zones": [
                {"name": "zoneA", "multiplicity": 10},
                {"name": "zoneB", "owner": "player", "multiplicity": 10}
            ]
        }

        self.game.load_config(config)

        # First we should have 20 zones, 10 of "zoneA"
        # and 10 "zoneB"s belonging to "player"
        self.assertEqual(len(self.game.zones), 20)

        # The ownerless zones should simply be numbered in order
        for i in range(1, 11):
            self.assertEqual(self.game.zones["zoneA" +
                                             str(i)], getattr(self.game, "zoneA" + str(i)))

        # Zones assigned to "player" should be numbered and include its game_id
        # "Player" should have attributes for its zones
        for i in range(11, 21):
            self.assertTrue(hasattr(self.player, "zoneB" + str(i)))
            self.assertEqual(self.game.zones["zoneB" + str(i) +
                                             "_" + str(self.game.player.game_id)],
                             getattr(self.player, "zoneB" + str(i)))

        other_player = self.game.add_player()

        # Now there are 30 zones, because "other_player" also has 10 "zoneB"s
        self.assertEqual(len(self.game.zones), 30)

        # New zones should be numbered and tagged with other_player's game_id
        # The player should also be aware of them as attributes
        for i in range(21, 31):
            self.assertTrue(hasattr(self.game.players[other_player],
                                    "zoneB" + str(i)))
            self.assertEqual(self.game.zones["zoneB" + str(i) +
                                             "_" + str(other_player)],
                             getattr(self.other_player, "zoneB" + str(i)))

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

    @skip("not yet implemented")
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

        # Game should contain only the valid zones
        self.assertEqual(len(self.game.zones), 2)

        # Game should have attributes for the valid zones
        self.assertTrue(hasattr(self.game, "zone1"))
        self.assertTrue(hasattr(self.game, "zone2"))

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
