from unittest import TestCase

from engine.game_runner import load_game_definition


class MagicTestCase(TestCase):

    def setUp(self):
        self.game, config = load_game_definition("game_defs/magic")
        self.game.load_config(config)
        self.player1 = self.game.get_object_with_id("Player",
                                                    self.game.add_player())
        self.player2 = self.game.get_object_with_id("Player",
                                                    self.game.add_player())

    def test_set_up(self):
        deck1 = [("Forest", 30)]
        deck2 = [("Island", 30)]

        self.game.deck1 = deck1
        self.game.deck2 = deck2

        self.game.set_up()

        # Make sure both players have the right cards in hand and library
        self.assertEqual(self.game.players[0].library.get_num_cards(), 23)
        self.assertEqual(self.game.players[1].library.get_num_cards(), 23)

        self.assertEqual(self.game.players[0].hand.get_num_cards(), 7)
        self.assertEqual(self.game.players[1].hand.get_num_cards(), 7)

        self.assertEqual(self.game.players[0].library.peek().name, "Forest")
        self.assertEqual(self.game.players[1].library.peek().name, "Island")

        # Make sure player attributes were initalized correctly
        self.assertEqual(self.game.players[0].life, 20)
        self.assertEqual(self.game.players[1].life, 20)
