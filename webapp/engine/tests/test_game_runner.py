"""
This module contains any tests around the GameRunner.

NOTE: These are not intgeration tests. Games are generally mocked out.

"""

from unittest import TestCase

from engine import game_runner
from engine.core.exceptions import InvalidMoveException
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
        self.mock_game.make_action = MagicMock()
        self.mock_game.get_transitions = MagicMock()
        self.mock_game.get_requires_information = MagicMock()

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

        state = game_runner.get_state(self.game_id, 1)
        self.assertEqual(state, expected_state)
        self.mock_game.get_state.assert_called_with(player_id = 1,
                                                    serialize=True)

    def test_start_game(self):
        """
        Make sure we can start the game.
        """

        game_runner.start_game(self.game_id)
        self.mock_game.set_up_wrapper.assert_called_with()

    def test_add_remove_player(self):
        """
        Make sure we can add and remove a player.
        """

        player = game_runner.add_player(self.game_id)
        self.mock_game.add_player.assert_called_with()

        game_runner.remove_player(self.game_id, player)
        self.mock_game.remove_player.assert_called_with(player)

    def test_action(self):
        """
        Make sure we can run an action.
        """

        game_runner.make_action(self.game_id, foo = 'bar')
        self.mock_game.make_action.assert_called_with(foo = 'bar')


        self.mock_game.make_action.side_effect = InvalidMoveException("Bad")
        success, message = game_runner.make_action(self.game_id)

        self.assertFalse(success)
        self.assertEqual(message, "Bad")

    def test_get_transitions(self):
        """
        Make sure we can get transitions.
        """

        game_runner.get_transitions(self.game_id, 1)
        self.mock_game.get_transitions.assert_called_with(player_id = 1,
                                                          serialize = True)

    def test_get_requires_information(self):
        """
        Make sure we can get transitions.
        """

        game_runner.get_requires_information(self.game_id)
        self.mock_game.get_requires_information.assert_called_with()

    def test_has_game(self):
        """
        Make sure we can query the game runner to see if it has a game.
        """

        self.assertTrue(game_runner.has_game(self.game_id))
        self.assertFalse(game_runner.has_game(-1))
