"""
Contains any tests around the base stateful game object.
"""

from unittest import TestCase

from engine.game import Game
from engine.stateful_game_object import StatefulGameObject


class StatefulGameObjectTestCase(TestCase):

    """
    A simple test case for testing anything related to
    game objects that have important state.
    """

    def setUp(self):
        self.game = Game()
        self.stateful_game_object = StatefulGameObject()

        self.game.register([self.stateful_game_object])

    def test_change_state(self):
        """
        Make sure that when we change the state the change
        is registered in the game and that we can still set
        attributes without a game.
        """

        expected_state_changes = [(StatefulGameObject,
                                   self.stateful_game_object.game_id,
                                   "life",
                                   10)]

        self.stateful_game_object.life = 10

        self.assertEqual(self.stateful_game_object.life, 10)
        self.assertEqual(expected_state_changes,
                         self.game.get_state_changes())
