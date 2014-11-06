"""
Test all of the Django views used by deckr.
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from unittest import skip

from deckr.models import GameRoom


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

    @skip("Not yet implemented")
    def test_can_access(self):
        """
        Make sure we can access the page.
        """

        response = self.client.get(reverse('deckr.create_game'))
        self.assertEqual(response.status_code, 200)

    @skip("Not yet implemented")
    def test_submit_form(self):
        """
        Make sure that the form submits, and that it will reject invalid
        input.
        """

        form_data = {'game_id': 1}

        response = self.client.post(reverse('deckr.create_game'),
                                    form_data)
        self.assertTrue(GameRoom.objects.all().count() > 0)
        game = list(GameRoom.objects.all())[-1]
        self.assertRedirects(response, reverse('deckr.game', args=(game.id,)))

        # Test invalid form
        response = self.client.post(reverse('deckr.create_game'),
                                    {})
        self.assertFormError(response, 'form', 'game_id',
                             'This field is required')


class GamePageTestCase(TestCase):

    """
    Test the game page to make sure that it's working as intended.
    NOTE: This only tests the view functionality; alot of this page
    is in websockets.
    """

    def setUp(self):
        self.client = Client()

    @skip("Not yet implemented")
    def test_can_access(self):
        """
        Make sure we can access the page.
        """

        response = self.client.get(reverse('deckr.game'))
        self.assertEqual(response.status_code, 200)
