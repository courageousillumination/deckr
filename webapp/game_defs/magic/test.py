from unittest import TestCase

from engine.game_runner import load_game_definition


class MagicTestCase(TestCase):

    def setUp(self):
        self.game, config = load_game_definition("game_defs/dominion")
        self.game.load_config(config)
        self.player1 = self.game.get_object_with_id("Player",
                                                    self.game.add_player())
        self.player2 = self.game.get_object_with_id("Player",
                                                    self.game.add_player())
