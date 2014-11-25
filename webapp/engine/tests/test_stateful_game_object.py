"""
Contains any tests around the base stateful game object.
"""

from unittest import TestCase

from engine.game import Game
from engine.player import Player
from engine.stateful_game_object import StatefulGameObject


class StatefulGameObjectTestCase(TestCase):

    """
    A simple test case for testing anything related to
    game objects that have important state.
    """

    def setUp(self):
        self.game = Game()
        self.stateful_game_object = StatefulGameObject()
        self.stateful_game_object.game_object_type = "foo"
        self.game.register([self.stateful_game_object])

    def test_change_state(self):
        """
        Make sure that when we change the state the change
        is registered in the game and that we can still set
        attributes without a game.
        """

        expected_state_changes = [("set",
                                   "foo",
                                   self.stateful_game_object.game_id,
                                   "life",
                                   10)]

        self.stateful_game_object.life = 10

        self.assertEqual(self.stateful_game_object.life, 10)
        self.assertEqual(expected_state_changes,
                         self.game.get_public_transitions())

        # Make sure we can set an attribute even if game is None

        self.stateful_game_object.game = None
        self.stateful_game_object.life = 20
        self.assertEqual(self.stateful_game_object.life, 20)

    def test_player_values(self):
        """
        Make sure that we can set values for a specific player.
        """

        player = Player()
        self.game.register([player])

        # Make sure that we can't get any values from a default player object
        self.assertIsNone(self.stateful_game_object.get_value("visible", player))

        expected_state_changes = [("set",
                                   "foo",
                                   self.stateful_game_object.game_id,
                                   "visible",
                                   True)]

        # Add per player transition
        self.stateful_game_object.set_value("visible", True, player)

        self.assertIsNone(self.stateful_game_object.get_value("visible"))
        self.assertEqual(self.stateful_game_object.get_value("visible", player),
                         True)

        # Make sure the game got the right transitions
        self.assertEqual(expected_state_changes,
                         self.game.get_player_transitions(player.game_id))

        # Make sure we can get the proper dictionary representation
        self.assertDictEqual(self.stateful_game_object.to_dict(),
                             {'game_id': self.stateful_game_object.game_id})
        self.assertDictEqual(self.stateful_game_object.to_dict(player),
                             {'game_id': self.stateful_game_object.game_id,
                              'visible': True})

    def test_set_values(self):
        """
        Make sure that calling set_value and get_value without a player
        just pass through to get and setattr.
        """

        self.stateful_game_object.life = 10
        self.stateful_game_object.set_value("poison", 1)

        self.assertEqual(10, self.stateful_game_object.get_value("life"))
        self.assertEqual(1, self.stateful_game_object.poison)
