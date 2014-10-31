"""
Unit tests for deckr websockets.
"""

from django.test import TestCase
from unittest import skip
from socketio.virtsocket import Socket
from mock import MagicMock

from deckr.sockets import ChatNamespace, GameNamespace
from deckr.models import Player


class MockSocketIOServer(object):

    """
    Mock a SocketIO server
    """

    def __init__(self, *args, **kwargs):
        super(MockSocketIOServer, self).__init__(*args, **kwargs)
        self.sockets = {}

    def get_socket(self, socket_id=''):
        """
        Simple look up in the local dictionary.
        """

        return self.sockets.get(socket_id)


class MockSocket(Socket):

    """
    Simple mocke socket.
    """

    pass


class MockGameRunner(object):

    """
    Simple mock game runner.
    """

    pass


class SocketTestCase(TestCase):

    """
    A simple abstract test case for any socket tests. This creates
    a mock server and socket to make testing a little easier.
    """

    def setUp(self):
        self.server = MockSocketIOServer()
        self.environ = {}
        self.socket = MockSocket(self.server, {})
        self.socket.error = MagicMock()
        self.environ['socketio'] = self.socket


class ChatNamespaceTestCase(SocketTestCase):

    """
    Test the ChatNamespace for websockets.
    """

    def setUp(self):
        super(ChatNamespaceTestCase, self).setUp()

        self.namespace = ChatNamespace(self.environ, '/chat')
        self.namespace.broadcast_event = MagicMock()

    def test_chat(self):
        """
        Make sure that if we chat a message it is broadcast to
        the entire namespace.
        """

        message = "hello world"

        self.namespace.on_chat(message)
        self.namespace.broadcast_event.assert_called_with("chat", message)


class GameNamespaceTestCase(SocketTestCase):

    """
    Test all the socket code around actually running the game.
    """

    def setUp(self):
        super(GameNamespaceTestCase, self).setUp()

        self.namespace = GameNamespace(self.environ, '/game')
        # Make sure we don't actually need to broadcast/emit events
        self.namespace.broadcast_event = MagicMock()
        self.namespace.emit = MagicMock()
        # Mock out the game runner
        self.namespace.runner = MockGameRunner()

    @skip("Not yet implemented")
    def test_invalid_move(self):
        """
        If we send an invalid move we should get an error.
        """

        invalid_move = "invalid"

        self.namespace.on_action(invalid_move)
        self.namespace.emit.assert_called_with("error", "ERROR")

    @skip("Not yet implemented")
    def test_valid_move(self):
        """
        If we send a valid move we should get a list of transitions.
        """

        valid_move = "valid move"
        transitions = [{}]

        self.namespace.on_action(valid_move)
        self.namespace.broadcast_event.assert_called_with("state_transition",
                                                          transitions)

    @skip("Not yet implemented")
    def test_request_state(self):
        """
        If we request the state, we should recieve the state back.
        """

        state = {'foo': 'bar'}

        self.namespace.on_request_state()
        self.namespace.emit.assert_called_with("state", state)

    @skip("Not yet implemented")
    def test_connect(self):
        """
        Make sure that when we get a socket connection we create a player
        for that socket.
        """

        old_count = Player.objects.all().count()
        self.namespace.on_connect()
        self.assertEqual(Player.objects.all().count(), old_count + 1)

    @skip("Not yet implemented")
    def test_disconnect(self):
        """
        If a player disconnects from the room we should clean up the player
        associated with them.
        """

        old_count = Player.objects.all().count()
        self.namespace.player = Player.objects.create(
            game_id=0,
            nickname="Bob")

        self.namespace.on_disconnect()
        self.assertEqual(Player.objects.all().count(), old_count)
