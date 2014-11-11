"""
Test all of the Django views used by deckr.
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from deckr.models import GameRoom, GameDefinition, Player


class IndexTestCase(TestCase):

    """
    Test the index page to make sure it's working as intended.
    """

    def setUp(self):
        self.client = Client()

    def test_can_access(self):
        """
        Make sure we can access the page.
        """

        response = self.client.get(reverse('deckr.index'))
        self.assertEqual(response.status_code, 200)


class CreateGameTestCase(TestCase):

    """
    Test the create game page to make sure it's working as intended.
    """

    def setUp(self):
        self.client = Client()

        # Make sure we have a game definition
        self.game_def = GameDefinition.objects.create(name="test",
                                                      path="/test")

    def test_can_access(self):
        """
        Make sure we can access the page.
        """

        response = self.client.get(reverse('deckr.create_game_room'))
        self.assertEqual(response.status_code, 200)

    def test_submit_form(self):
        """
        Make sure that the form submits, and that it will reject invalid
        input.
        """

        form_data = {'game_id': self.game_def.pk}

        response = self.client.post(reverse('deckr.create_game_room'),
                                    form_data)
        self.assertTrue(GameRoom.objects.all().count() > 0)
        game = list(GameRoom.objects.all())[-1]
        self.assertRedirects(response,
                             reverse('deckr.game_room_staging_area',
                                     args=(game.id,)))

        # Test invalid form
        response = self.client.post(reverse('deckr.create_game_room'),
                                    {})
        self.assertFormError(response, 'form', 'game_id',
                             'This field is required.')

        response = self.client.post(reverse('deckr.create_game_room'),
                                    {'game_id': 0})
        self.assertFormError(response, 'form', 'game_id',
                             "Select a valid choice. That choice is not one" +
                             " of the available choices.")


class GamePageTestCase(TestCase):

    """
    Test the game page to make sure that it's working as intended.
    NOTE: This only tests the view functionality; a lot of this page
    is in websockets.
    """

    def setUp(self):
        self.client = Client()
        self.game_room = GameRoom.objects.create(room_id=1)
        self.player = Player.objects.create(game_room=self.game_room,
                                            player_id=1,
                                            nickname="Player 1")

    def test_can_access(self):
        """
        Make sure we can access the page.
        """

        response = self.client.get(reverse('deckr.game_room',
                                           args=(self.game_room.pk,)),
                                   {'player_id': self.player.id})
        self.assertEqual(response.status_code, 200)
