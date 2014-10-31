"""
Test all of the Django views used by deckr.
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from unittest import skip


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

    @skip
    def test_can_access(self):
        """
        Make sure we can access the page.
        """

        response = self.client.get(reverse('deckr.create_game'))
        self.assertEqual(response.status_code, 200)


class GamePageTestCase(TestCase):

    """
    Test the game page to make sure that it's working as intended.
    NOTE: This only tests the view functionality; alot of this page
    is in websockets.
    """

    def setUp(self):
        self.client = Client()

    @skip
    def test_can_access(self):
        """
        Make sure we can access the page.
        """

        response = self.client.get(reverse('deckr.game'))
        self.assertEqual(response.status_code, 200)
