"""
This module contains any tests around the GameRunner. This is a harder
class to test because it's stateful, so make sure you're careful about
that. Note that the game runner is a __module__ not a class (this is
the best way we could think of to implement the singleton pattern).
"""

from unittest import TestCase,skip

from engine import game_runner
from engine.game import Game
from engine.player import Player
from engine.tests.mock_game.mock_game import MockGame


class GameRunnerTestCase(TestCase):

    """
    A pretty straightforward test case for the GameRunner.
    """

    def setUp(self):
        self.valid_game_def = "engine/tests/mock_game"
        self.game_id = game_runner.create_game(self.valid_game_def)

    def tearDown(self):
        game_runner.flush()

    def test_load_game_definition(self):
        """
        Makes sure we can load a game definition. A definition should
        minimally consisty of a game.py and a config.yml.
        """

        game, config = game_runner.load_game_definition(self.valid_game_def)
        self.assertDictEqual(config, {"game_file": "mock_game",
                                      "game_class": "MockGame",
                                      "max_players": 1})
        self.assertTrue(isinstance(game, Game))
        # This has been disabled due to namespacing issues. It really is a
        # mock_game but python doesn't belive it. Instead I've put in MAGIC
        # test.
        # self.assertTrue(type(game, MockGame))
        self.assertEqual(game.get_magic(), MockGame().get_magic())

        # Make sure we fail properly if we give it a bad folder
        self.assertRaises(IOError, game_runner.load_game_definition, "foo")

        # Make sure we get a value error if it's misconfigured
        self.assertRaises(ValueError, game_runner.load_game_definition,
                          "engine/tests/invalid_game_config")

    def test_create_room(self):
        """
        Test the ability to create a game room.
        """

        self.assertRaises(IOError, game_runner.create_game,
                          "invalid file")

        game_id = game_runner.create_game(self.valid_game_def)
        self.assertTrue(game_id > 0)

        # Make sure IDs are unique
        game_id_1 = game_runner.create_game(self.valid_game_def)
        self.assertNotEqual(game_id, game_id_1)

    def test_destroy_room(self):
        """
        Make sure that we can destroy a game room.
        """

        game_id = game_runner.create_game(self.valid_game_def)
        game_runner.destroy_game(game_id)
        self.assertFalse(game_runner.has_game(game_id))

    def test_get_state(self):
        """
        Makes sure we can get the state out of a game.
        """
        expected_state = {'cards': [], 'zones': [], 'players': []}

        game_id = game_runner.create_game(self.valid_game_def)
        state = game_runner.get_state(game_id)
        self.assertEqual(state, expected_state)

    def test_add_player(self):
        """
        Makes sure that we can add a player and get back a valid
        id.
        """

        game_runner.get_game(self.game_id).max_players = 2
        player_id = game_runner.add_player(self.game_id)
        self.assertTrue(player_id > 0)
        self.assertNotEqual(player_id,
                            game_runner.add_player(self.game_id))

    @skip
    def test_remove_player(self):
        """
        Makes sure we can remove a player and it informs
        if we are successful or not
        """

        game_runner.add_player(self.game_id)
        player_id = game_runner.get_game(self.game_id).players[0].game_id
        self.assertTrue(game_runner.remove_player(self.game_id, player_id))
        self.assertFalse(game_runner.remove_player(self.game_id, player_id))
        player_id = game_runner.add_player(self.game_id)

    def test_start_game(self):
        """
        Make sure that we can start a game and when we do so no transitions
        are stored.
        """

        game_runner.start_game(self.game_id)
        self.assertTrue(game_runner.get_game(self.game_id).is_setup)
        self.assertEqual(game_runner.get_game(self.game_id).transitions, [])

    def test_make_action(self):
        """
        Make sure that we can make actions through the GameRunner.
        """

        game1 = game_runner.get_game(self.game_id)
        game1.phase = "restricted"
        player = Player()
        game1.register([player])
        action = "restricted_action"

        error, message = game_runner.make_action(self.game_id,
                                                 action_name=action,
                                                 player_id=player.game_id)
        self.assertTrue(error)
        self.assertEqual(message, "Illegal Action")

        game1.phase = "unrestricted"

        self.assertEqual((False, [('is_over', [player.game_id])]),

                         game_runner.make_action(self.game_id,
                                                 action_name=action,
                                                 player_id=player.game_id))
