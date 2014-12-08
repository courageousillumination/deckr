from unittest import skip, TestCase

from engine.game import InvalidMoveException
from engine.game_runner import load_game_definition
from magic import create_mana_from_string, Mana


class ManaTestCase(TestCase):
    """
    Test the Mana object.
    """

    def test_negative_creation(self):
        self.assertRaises(ValueError, Mana, red = -1)

    def test_creation_from_string(self):
        mana = create_mana_from_string("RWGBU")

        self.assertEqual(mana.red, 1)
        self.assertEqual(mana.blue, 1)
        self.assertEqual(mana.green, 1)
        self.assertEqual(mana.white, 1)
        self.assertEqual(mana.black, 1)

        self.assertEqual("WUBRG", mana.__str__())

    def test_addition(self):
        mana1 = Mana(blue = 3)
        mana2 = Mana(blue = 1, white = 1)

        result_mana = mana1 + mana2
        self.assertEqual(result_mana.blue, 4)
        self.assertEqual(result_mana.white, 1)

        mana1 += mana2
        self.assertEqual(mana1.blue, 4)
        self.assertEqual(mana1.white, 1)

    def test_subtraction(self):
        mana1 = Mana(blue = 3)
        mana2 = Mana(blue = 1)

        result_mana = mana1 - mana2
        self.assertEqual(result_mana.blue, 2)

        mana1 -= mana2
        self.assertEqual(mana1.blue, 2)

    def test_cmc(self):
        mana = create_mana_from_string("RWGBU")
        self.assertEqual(mana.converted_mana(), 5)


class MagicTestCase(TestCase):

    def setUp(self):
        self.game, config = load_game_definition("game_defs/magic")
        self.game.load_config(config)
        self.player1 = self.game.get_object_with_id("Player",
                                                    self.game.add_player())
        self.player2 = self.game.get_object_with_id("Player",
                                                    self.game.add_player())

        deck1 = [("Forest", 30)]
        deck2 = [("Island", 30)]

        self.game.deck1 = deck1
        self.game.deck2 = deck2

        self.game.set_up()

    def test_set_up(self):
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

    def test_pass_priority(self):
        """
        Make sure we can pass priority from one player to another and that
        the phase or step update accordingly.
        """

        # To begin with we should be in the beginning phase, upkeep step
        self.game.step = "upkeep"
        self.game.phase = "beginning"
        self.game.active_player = self.player1
        self.game.has_priority_player = self.player1

        # Now we pass twice and we should be in the draw step
        self.game.pass_priority(self.player1)
        self.game.pass_priority(self.player2)

        self.assertEqual(self.game.step, "draw")
        self.assertEqual(self.game.phase, "beginning")

        # Now when we pass priority here we should be in precombat main phase
        self.game.pass_priority(self.player1)
        self.game.pass_priority(self.player2)

        self.assertEqual(self.game.step, None)
        self.assertEqual(self.game.phase, "precombat_main")

        # Pass again into the combat phase
        self.game.pass_priority(self.player1)
        self.game.pass_priority(self.player2)

        self.assertEqual(self.game.step, "beginning_of_combat")
        self.assertEqual(self.game.phase, "combat")

        # Now we move on to declare attackers
        self.game.pass_priority(self.player1)
        self.game.pass_priority(self.player2)

        self.assertEqual(self.game.step, "declare_attackers")
        self.assertEqual(self.game.phase, "combat")

        # Nobody was declared as attacking so we skip right to the end of combat
        self.game.pass_priority(self.player1)
        self.game.pass_priority(self.player2)

        self.assertEqual(self.game.step, "end_of_combat")
        self.assertEqual(self.game.phase, "combat")

        # Next we move on to the second main phase
        self.game.pass_priority(self.player1)
        self.game.pass_priority(self.player2)

        self.assertEqual(self.game.step, None)
        self.assertEqual(self.game.phase, "postcombat_main")

        # Finally we go to the end phase
        self.game.pass_priority(self.player1)
        self.game.pass_priority(self.player2)

        self.assertEqual(self.game.step, "end")
        self.assertEqual(self.game.phase, "end")

        # Clean up phase
        self.game.pass_priority(self.player1)
        self.game.pass_priority(self.player2)

        self.assertEqual(self.game.step, "cleanup")
        self.assertEqual(self.game.phase, "end")

    def test_play_land(self):
        # First we'll cheat and say that it's the precombat main phase
        self.game.phase = "precombat_main"
        self.game.step = None

        card = self.player1.hand.get_cards()[0]

        # Now we try to play one of the lands in our hand
        self.game.play_card(self.player1, card)

        # It should be on the battlefield
        self.assertIn(card, self.player1.battlefield)

        # Make sure we can't play another one
        self.assertRaises(InvalidMoveException, self.game.play_card,
                          self.player1,
                          self.player1.hand.get_cards()[0])

    def test_activate_land(self):

        self.game.phase = "precombat_main"
        self.game.step = None

        card = self.player1.hand.get_cards()[0]
        self.game.play_card(self.player1, card)

        # Now try to activate the cards ability
        self.game.activate_ability(self.player1, card)

        self.assertEqual(self.player1.mana_pool.green, 1)
        self.assertTrue(card.tapped)
