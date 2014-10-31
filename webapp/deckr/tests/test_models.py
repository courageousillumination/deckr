"""
Test cases for all of our models.
"""

from django.test import TestCase
from unittest import skip

from deckr.models import GameRoom, Player


class GameRoomTestCase(TestCase):

    """
    Test the GameRoom model and its associated hooks.
    """

    def setUp(self):
        self.game_room = GameRoom.objects.create(room_id=1,
                                                 max_players=2)

    @skip("Not yet implemented")
    def test_string_representation(self):
        """
        Make sure that the string representation of the GameRoom works.
        """

        self.assertEqual(self.game_room.__unicode__(), "Game room for game 1")

    @skip("Not yet implemented")
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
        try:
            Player.objects.create(player_id=2,
                                  nickname="Alice",
                                  game_room=self.game_room)
            self.fail()
        except ValueError:
            pass

        player1.delete()
        player2.delete()

    @skip("Not yet implemented")
    def test_duplicate_nicknames(self):
        """
        Make sure that we can't have two players with the same nickname.
        """

        player1 = Player.objects.create(player_id=1,
                                        nickname="Bob",
                                        game_room=self.game_room)
        try:
            Player.objects.create(player_id=2,
                                  nickname="Bob",
                                  game_room=self.game_room)
            self.fail()
        except ValueError:
            pass

        player1.delete()


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

    @skip("Not yet implemented")
    def test_string_representation(self):
        """
        Make sure that the string representation of the GameRoom works.
        """

        self.assertEqual(self.player.__unicode__(), "Bob")

    @skip("Not yet implemented")
    def test_nickname(self):
        """
        Make sure that the nickname will reject invalid values.
        """

        # Nicknames can't be empty
        self.player.nickname = ""
        try:
            self.player.save()
            self.fail()
        except ValueError:
            pass
