"""
This module provides tests that integrate a set of functionality.
It provides a simple game and then attempts to play that game
using the interface provided by the game_runner.
"""

import os
from unittest import TestCase

from engine import game_runner


class IntegrationTestCase(TestCase):

    """
    Run several integration tests.
    """

    @classmethod
    def setUpClass(cls):
        """
        We really only need to read in the file once.
        """

        base_path = os.path.dirname(os.path.realpath(__file__))
        game_definition = os.path.join(base_path, 'test_game')
        klass, config = game_runner.load_game_definition(game_definition)
        cls._klass = klass
        cls._config = config

    def setUp(self):
        self.game_id = game_runner.create_game_internal(self._klass,
                                                        self._config)
        self.game = game_runner.get_game(self.game_id)

        self.player1_id = game_runner.add_player(self.game_id)
        self.player2_id = game_runner.add_player(self.game_id)
        self.player1 = self.game.get_object_with_id(self.player1_id)
        self.player2 = self.game.get_object_with_id(self.player2_id)

        game_runner.start_game(self.game_id)

    def tearDown(self):
        game_runner.flush()

    def test_set_up(self):
        """
        Make sure the game got properly set up.
        """

        self.assertTrue(self.game.is_set_up)

    def test_get_state(self):
        """
        Make sure the various zones, players, etc. were registered.
        """

        shared_expected_objects = [
            {'game_object_type': 'Game', 'game_id': 0},
            # Both players can see both players
            {'game_object_type': 'Player', 'game_id': self.player1_id},
            {'game_object_type': 'Player', 'game_id': self.player2_id},
            # Both players can see the game zone
            {'game_object_type': 'Zone', 'owner': 0, 'name': 'game_zone',
             'game_id': self.game.game_zone.game_id},
            # Both players can see each other's zones
            {'game_object_type': 'Zone', 'owner': self.player1_id,
             'name': 'player_zone',
             'game_id': self.player1.player_zone.game_id},
            {'game_object_type': 'Zone', 'owner': self.player2_id,
             'name': 'player_zone',
             'game_id': self.player2.player_zone.game_id},
        ]

        player1_expected_objects = [
            {'game_id': self.game.foo_object.game_id,
             'game_object_type': 'FooObject', 'foo': 'baz'}
        ]
        player2_expected_objects = [
            {'game_id': self.game.foo_object.game_id,
             'game_object_type': 'FooObject', 'foo': 'bar'}
        ]

        player1_state = game_runner.get_state(self.game_id, self.player1_id)
        player2_state = game_runner.get_state(self.game_id, self.player2_id)

        for obj in shared_expected_objects:
            self.assertIn(obj, player1_state)
            self.assertIn(obj, player2_state)

        for obj in player1_expected_objects:
            self.assertIn(obj, player1_state)

        for obj in player2_expected_objects:
            self.assertIn(obj, player2_state)

    def test_per_player_transition(self):
        """
        Make sure that we can add transitions on a per player basis.
        """

        self.game.transitions = {}

        game_runner.make_action(self.game_id, action_name='change_foo',
                                player_id=self.player1_id,
                                new_foo_value='woo!')
        player1_transitions = game_runner.get_transitions(self.game_id,
                                                          self.player1_id)
        player2_transitions = game_runner.get_transitions(self.game_id,
                                                          self.player2_id)

        self.assertEqual([{'name': 'set', 'attribute': 'foo', 'value': 'woo!',
                           'game_id': self.game.foo_object.game_id,
                           'class': 'FooObject'}], player1_transitions)
        self.assertEqual([], player2_transitions)
