"""
Test cases for all of our models.
"""

from django.test import TestCase
from deckr.models import GameRoom, Player, GameDefinition


class GameDefinitionTestCase(TestCase):

    """
    Test any logic pertaining to the game definition class.
    """

    def setUp(self):
        self.definition = GameDefinition.objects.create(name="foo",
                                                        path="/bar")

    def test_string_representation(self):
        """
        Make sure the string representation is valid.
        """

        self.assertEqual(self.definition.__unicode__(),
                         "foo")


class GameRoomTestCase(TestCase):

    """
    Test the GameRoom model and its associated hooks.
    """

    def setUp(self):
        self.game_room = GameRoom.objects.create(room_id=1,
                                                 max_players=2)

    def test_string_representation(self):
        """
        Make sure that the string representation of the GameRoom works.
        """

        self.assertEqual(self.game_room.__unicode__(),
                         "Game room 1 for the game Solitaire")

    def test_add_players(self):
        """
        Make sure we can add players if there is room, and that we throw
        an exception if there are already too many players.
        """

        player1 = Player.objects.create(player_id=1,
                                        nickname="Bob",
                                        game_room=self.game_room)
        player2 = Player.objects.create(player_id=2,
                                        nickname="Carol",
                                        game_room=self.game_room)

        self.assertIn(player1, self.game_room.player_set.all())
        self.assertIn(player2, self.game_room.player_set.all())

        # Can't have more than max players
        self.assertRaises(ValueError, Player.objects.create,
                          player_id=3, nickname="Alice",
                          game_room=self.game_room)
        player1.delete()
        player2.delete()

    def test_duplicate_nicknames(self):
        """
        Make sure that we can't have two players with the same nickname.
        """

        player1 = Player.objects.create(player_id=1,
                                        nickname="Bob",
                                        game_room=self.game_room)
        self.assertRaises(ValueError, Player.objects.create,
                          player_id=2, nickname="Bob",
                          game_room=self.game_room)

        player1.delete()

    def test_maximum_occupancy(self):
        """
        Make sure a player cannot join a full room
        """
        game_room = GameRoom.objects.create(room_id=1,
                                            max_players=0)
        self.assertTrue(game_room.maximum_occupancy())

        game_room.max_players = 1

        self.assertFalse(game_room.maximum_occupancy())

        Player.objects.create(player_id=1,
                              nickname="Bob",
                              game_room=game_room)

        self.assertTrue(game_room.maximum_occupancy())

    def test_existing_nickname(self):
        """
        Make sure nicknames in a room are unique
        """
        Player.objects.create(player_id=1,
                              nickname="Bob",
                              game_room=self.game_room)

        self.assertTrue(self.game_room.existing_nickname("Bob"))
        self.assertFalse(self.game_room.existing_nickname("Alice"))


class PlayerTestCase(TestCase):

    """
    Test the Player model.
    """

    def setUp(self):
        self.game_room = GameRoom.objects.create(room_id=1,
                                                 max_players=2)
        self.player = Player.objects.create(player_id=1,
                                            nickname="Bob",
                                            game_room=self.game_room)

    def test_string_representation(self):
        """
        Make sure that the string representation of the GameRoom works.
        """

        self.assertEqual(self.player.__unicode__(), "Bob")

    def test_nickname(self):
        """
        Make sure that the nickname will reject invalid values.
        """

        # Nicknames can't be empty
        self.player.nickname = ""
        self.assertRaises(ValueError, self.player.save)
