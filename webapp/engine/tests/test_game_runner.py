"""
This module contains any tests around the GameRunner.

NOTE: These are not intgeration tests. Games are generally mocked out.

"""

from unittest import TestCase

from engine import game_runner
from mock import MagicMock


class MockGame(object):
    pass

class GameRunnerTestCase(TestCase):

    """
    A pretty straightforward test case for the GameRunner.
    """

    def setUp(self):
        # Add a single game using game_id = 1
        self.game_id = 1
        self.mock_game = MockGame()
        self.mock_game.get_state = MagicMock()
        self.mock_game.add_player = MagicMock()
        self.mock_game.remove_player = MagicMock()
        self.mock_game.set_up_wrapper = MagicMock()

        game_runner.CACHE[self.game_id] = self.mock_game

        #self.valid_game_def = "engine/tests/mock_game"
        #self.game_id = game_runner.create_game(self.valid_game_def)

    def tearDown(self):
        game_runner.flush()

    def test_get_game(self):
        """
        Make sure we can get a game by id.
        """

        self.assertEqual(self.mock_game, game_runner.get_game(self.game_id))
        self.assertIsNone(game_runner.get_game(-1))


    def test_destroy_game(self):
        """
        Make sure that we can destroy a game.
        """

        game_runner.destroy_game(self.game_id)
        self.assertFalse(game_runner.has_game(self.game_id))

        # Make sure it fails silently if we delete a nonexistent game.
        game_runner.destroy_game(-1)

    def test_get_state(self):
        """
        Makes sure we can get the state out of a game.
        """
        expected_state = [{'foo': 'bar'}]
        self.mock_game.get_state.return_value = expected_state

        state = game_runner.get_state(self.game_id)
        self.assertEqual(state, expected_state)
        self.mock_game.get_state.ssert_called_with()

    def test_start_game(self):
        """
        Make sure we can start the game.
        """

        game_runner.start_game(self.game_id)
        self.mock_game.set_up_wrapper.ssert_called_with()

    def test_add_remove_player(self):
        """
        Make sure we can add and remove a player.
        """

        player = game_runner.add_player(self.game_id)
        self.mock_game.add_player.ssert_called_with()

        game_runner.remove_player(self.game_id, player)
        self.mock_game.remove_player.ssert_called_with(player)
