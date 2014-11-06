"""
Unit tests for deckr websockets.
"""

from django.test import TestCase
from unittest import skip
from socketio.virtsocket import Socket
from mock import MagicMock

from deckr.sockets import ChatNamespace, GameNamespace
from deckr.models import Player, GameRoom


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
        self.namespace.runner.add_player = MagicMock()
        self.namespace.runner.get_state = MagicMock()

        self.game_room = GameRoom.objects.create(room_id=0,
                                                 max_players=1)

        self.namespace.on_join(str(self.game_room.pk))

    def test_join(self):
        """
        Make sure that when we get a socket connection we create a player
        for that socket.
        """

        # Discard the already joined data
        self.namespace.flush()

        old_count = Player.objects.all().count()
        self.assertTrue(self.namespace.on_join(str(self.game_room.pk)))
        self.assertEqual(Player.objects.all().count(), old_count + 1)
        self.namespace.runner.add_player.assert_called()

        # Make sure we can't join a full room
        self.assertFalse(self.namespace.on_join(str(self.game_room.pk)))
        self.assertEqual(Player.objects.all().count(), old_count + 1)
        self.namespace.emit.assert_called_with("error",
                                               "Unable to join game room.")

        # Make sure we can't join a bad room id
        self.assertFalse(self.namespace.on_join("0"))
        self.assertEqual(Player.objects.all().count(), old_count + 1)
        self.namespace.emit.assert_called_with("error",
                                               "Can not find game room")

        # Make sure we can't join a bad room id
        self.assertFalse(self.namespace.on_join("foo"))
        self.assertEqual(Player.objects.all().count(), old_count + 1)
        self.namespace.emit.assert_called_with("error",
                                               "Room id is not an integer.")

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

    def test_request_state(self):
        """
        If we request the state, we should recieve the state back.
        """

        state = {'foo': 'bar'}

        # Mock out the runner
        runner = self.namespace.runner
        runner.get_state.return_value = state

        self.namespace.on_request_state({})
        self.namespace.emit.assert_called_with("state", state)
        runner.get_state.assert_called_with(self.game_room.room_id)

    def test_disconnect(self):
        """
        If a player disconnects from the room we should clean up the player
        associated with them.
        """

        old_count = Player.objects.all().count()
        self.namespace.recv_disconnect()
        self.assertEqual(Player.objects.all().count(), old_count - 1)

        # Make sure we reconnect.
        self.namespace.player = Player.objects.create(
            game_room=self.game_room,
            player_id=0,
            nickname="Bob")
