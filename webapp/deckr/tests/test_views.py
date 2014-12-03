"""
Test all of the Django views used by deckr.
"""

import tempfile

from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.test.utils import override_settings

import deckr.views
from deckr.models import GameDefinition, GameRoom, Player
from mock import MagicMock

MOCK_GAME = "engine/tests/mock_game"


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
                                                      path=MOCK_GAME)

    def test_can_access(self):
        """
        Make sure we can access the page.
        """

        response = self.client.get(reverse('deckr.create_game_room'))
        self.assertEqual(response.status_code, 200)

    def test_create_game_form(self):
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


class CreatePlayerTestCase(TestCase):

    """
    Test the create player form to join a game room
    """

    def setUp(self):
        self.client = Client()

        # Make sure we have a game definition
        self.game_def = GameDefinition.objects.create(name="test",
                                                      path=MOCK_GAME)
        self.game_room = GameRoom.objects.create(game_definition=self.game_def,
                                                 room_id=1,
                                                 max_players=1)

        # Mock out the add player function
        deckr.views.game_runner = MagicMock()

    def test_can_access(self):
        """
        Make sure we can access the form.
        """

        response = self.client.get(reverse('deckr.game_room_staging_area',
                                           args=(self.game_room.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_out_of_sync_engine(self):
        """
        Make sure that even if the engine throws an internal error
        while creating a player that we catch it and return a valid
        page instead of throwing a stacktrace.
        """

        error_msg = "Failed to join"
        deckr.views.game_runner.add_player.side_effect = ValueError(error_msg)
        form_data = {'nickname': "Player 1"}
        response = self.client.post(reverse('deckr.game_room_staging_area',
                                            args=(self.game_room.pk,)),
                                    form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'nickname', error_msg)

    def test_create_player_form(self):
        """
        Check form validations and player creation
        """

        deckr.views.game_runner.add_player.return_value = 1

        form_data = {'nickname': "Player 1"}

        response = self.client.post(reverse('deckr.game_room_staging_area',
                                            args=(self.game_room.pk,)),
                                    form_data)
        player = list(Player.objects.all())[-1]
        self.assertTrue(Player.objects.all().count() > 0)
        self.assertRedirects(response,
                             reverse('deckr.game_room',
                                     args=(self.game_room.id,)) +
                             "?player_id=" + str(player.pk))

        old_count = Player.objects.all().count()
        response = self.client.post(reverse('deckr.game_room_staging_area',
                                            args=(self.game_room.pk,)),
                                    form_data)
        self.assertEqual(Player.objects.all().count(), old_count)
        self.assertFormError(response, 'form', 'nickname',
                             'Nickname is already in use')

        response = self.client.post(reverse('deckr.game_room_staging_area',
                                            args=(self.game_room.pk,)),
                                    {})
        self.assertFormError(response, 'form', 'nickname',
                             'This field is required.')
        self.assertEqual(Player.objects.all().count(), old_count)

        old_count = Player.objects.all().count()
        form_data = {'nickname': "Player 2"}
        response = self.client.post(reverse('deckr.game_room_staging_area',
                                            args=(self.game_room.pk,)),
                                    form_data)
        self.assertEqual(Player.objects.all().count(), old_count)
        self.assertFormError(response, 'form', 'nickname',
                             'Cannot join full room')


class GamePageTestCase(TestCase):

    """
    Test the game page to make sure that it's working as intended.
    NOTE: This only tests the view functionality; a lot of this page
    is in websockets.
    """

    def setUp(self):
        self.client = Client()
        self.game_def = GameDefinition.objects.create(name="test",
                                                      path=MOCK_GAME)
        self.game_room = GameRoom.objects.create(room_id=1,
                                                 game_definition=self.game_def)
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


class UploadGameDefTestCase(TestCase):

    """
    Test the upload game page to submit a zipped file and create a game
    definition
    """

    def setUp(self):
        self.client = Client()

    def test_can_access(self):
        """
        Make sure we can access the page.
        """

        response = self.client.get(reverse('deckr.upload_game_definition'))
        self.assertEqual(response.status_code, 200)


    @override_settings(GAME_DEFINITION_PATH=tempfile.mkdtemp())
    def test_can_upload(self):
        """
        Make sure the form submits or displays validation
        """



        old_count = GameDefinition.objects.all().count()
        form_data = {'game_name': 'Solitaire',
                     'file': open('deckr/tests/solitaire.zip')}
        response = self.client.post(reverse('deckr.upload_game_definition',),
                                    form_data)
        self.assertEqual(GameDefinition.objects.all().count(), old_count + 1)

        old_count = GameDefinition.objects.all().count()
        response = self.client.post(reverse('deckr.upload_game_definition',),
                                    {})
        self.assertFormError(response, 'form', 'file',
                             'This field is required.')
        self.assertEqual(GameDefinition.objects.all().count(), old_count)

        old_count = GameDefinition.objects.all().count()

        # Test a zipped file that is missing the layout.html
        form_data = {'game_name': 'Solitaire',
                     'file': open('deckr/tests/failing_solitaire.zip')}
        response = self.client.post(reverse('deckr.upload_game_definition',),
                                    form_data)
        self.assertEqual(GameDefinition.objects.all().count(), old_count)
