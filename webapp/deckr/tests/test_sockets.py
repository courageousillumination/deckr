"""
Unit tests for deckr websockets.
"""

from django.test import TestCase
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
        self.namespace.emit_to_room = MagicMock()
        # Mock out the game runner
        self.namespace.runner = MockGameRunner()
        self.namespace.runner.add_player = MagicMock()
        self.namespace.runner.add_player.return_value = 0
        self.namespace.runner.get_state = MagicMock()
        self.namespace.runner.make_action = MagicMock()
        self.namespace.runner.start_game = MagicMock()
        self.game_room = GameRoom.objects.create(room_id=0,
                                                 max_players=1)
        self.player = Player.objects.create(player_id=1,
                                            nickname="Player 1",
                                            game_room=self.game_room)

        request = {
            'game_room_id': str(
                self.game_room.pk),
            'player_id': self.player.id}
        self.namespace.on_join(request)

    def test_join(self):
        """
        Make sure that when we get a socket connection we create a player
        for that socket.
        """

        # Discard the already joined data
        self.namespace.flush()

        self.player = Player.objects.create(player_id=1,
                                            nickname="Player 1",
                                            game_room=self.game_room)

        request = {'game_room_id': str(self.game_room.pk),
                   'player_id': self.player.id}
        self.assertTrue(self.namespace.on_join(request))
        self.namespace.runner.add_player.assert_called()
        player_names = [{'nickname': p.nickname, 'id': p.player_id}
                        for p in self.game_room.player_set.all()]

        self.namespace.emit_to_room.assert_called_with(self.namespace.room,
                                                       'player_names',
                                                       player_names)

        # Make sure we can't join a bad room id
        request = {'game_room_id': "0", 'player_id': self.player.id}
        self.assertFalse(self.namespace.on_join(request))
        self.namespace.emit.assert_called_with("error",
                                               "Can not find game room")

        # Make sure we can't join a bad room id
        request = {'game_room_id': "foo", 'player_id': self.player.id}
        self.assertFalse(self.namespace.on_join(request))
        error_message = "Game room id is not an integer."
        self.namespace.emit.assert_called_with("error", error_message)

    def test_invalid_move(self):
        """
        If we send an invalid move we should get an error.
        """

        invalid_move = {"action": "invalid"}

        self.namespace.runner.make_action.return_value = (True, "Invalid move")
        self.assertFalse(self.namespace.on_action(invalid_move))
        self.namespace.emit.assert_called_with("error", "Invalid move")

    def test_valid_move(self):
        """
        If we send a valid move we should get a list of transitions.
        """

        valid_move = {"action": "valid move"}
        transitions = [{}]
        self.namespace.runner.make_action.return_value = (False, transitions)

        self.namespace.on_action(valid_move)
        self.namespace.emit_to_room.assert_called_with(self.namespace.room,
                                                       "state_transitions",
                                                       transitions)

    def test_request_state(self):
        """
        If we request the state, we should recieve the state back.
        """

        state = {'foo': 'bar'}
        error = "Please connect to a game room first."

        # Mock out the runner
        runner = self.namespace.runner
        runner.get_state.return_value = state

        self.assertTrue(self.namespace.on_request_state())
        self.namespace.emit.assert_called_with("state", state)
        runner.get_state.assert_called_with(self.game_room.room_id)

        # Test that we get an error if we call this without a room
        self.namespace.game_room = None
        self.assertFalse(self.namespace.on_request_state())

        self.namespace.emit.assert_called_with("error", error)

    def test_update_player_list(self):
        """
        If a game room player list changes, broadcast the updated information
        to the room
        """

        self.namespace.update_player_list()
        player_names = [{'nickname': p.nickname, 'id': p.player_id}
                        for p in self.game_room.player_set.all()]
        self.namespace.emit_to_room.assert_called_with(self.namespace.room,
                                                       'player_names',
                                                       player_names)
        self.namespace.emit_to_room.reset_mock()

        self.namespace.game_room = None
        self.namespace.update_player_list()
        self.assertFalse(self.namespace.emit_to_room.called)

    def test_on_update_nickname(self):
        """
        If a player updates their nickname, handle the update and broadcast
        the change to the room
        """

        new_nickname = self.namespace.player.nickname + "_new"
        self.assertTrue(self.namespace.on_update_nickname(new_nickname))
        self.assertEqual(self.namespace.player.nickname, new_nickname)
        player_names = [{'nickname': p.nickname, 'id': p.player_id}
                        for p in self.game_room.player_set.all()]
        self.namespace.emit_to_room.assert_called_with(self.namespace.room,
                                                       'player_names',
                                                       player_names)

        same_nickname = self.namespace.player.nickname
        self.assertFalse(self.namespace.on_update_nickname(same_nickname))
        self.namespace.emit.assert_called_with("error", "Invalid nickname")

        self.namespace.game_room = None
        new_nickname = self.namespace.player.nickname + "_new"
        self.assertFalse(self.namespace.on_update_nickname(new_nickname))
        self.namespace.emit.assert_called_with(
            "error",
            "Please connect to a game room first.")

        self.namespace.player = None
        self.assertFalse(self.namespace.on_update_nickname(new_nickname))
        self.namespace.emit.assert_called_with(
            "error",
            "Please connect to a game room first.")

    def test_on_destroy_game(self):
        """
        If a player destroys the room, handle clean up
        """

        self.assertEqual(Player.objects.all().count(), 1)
        self.assertEqual(GameRoom.objects.all().count(), 1)
        self.assertTrue(self.namespace.on_destroy_game())
        self.assertEqual(Player.objects.all().count(), 0)
        self.assertEqual(GameRoom.objects.all().count(), 0)
        self.namespace.emit.assert_called_with('leave_game')
        self.namespace.emit_to_room.assert_called_with(str(self.game_room.id),
                                                       'leave_game')

    def test_on_leave_game(self):
        """
        If a player leaves the room, handle clean up
        """

        self.game_room.max_players = 2
        self.game_room.save()
        self.player = Player.objects.create(player_id=2,
                                            nickname="Player 2",
                                            game_room=self.game_room)

        request = {'game_room_id': str(self.game_room.pk),
                   'player_id': self.player.id}
        self.namespace.on_join(request)

        self.assertEqual(Player.objects.all().count(), 2)
        self.assertEqual(GameRoom.objects.all().count(), 1)
        self.assertTrue(self.namespace.on_leave_game())
        self.assertEqual(Player.objects.all().count(), 1)
        self.assertEqual(GameRoom.objects.all().count(), 1)
        self.namespace.emit.assert_called_with('leave_game')

        self.namespace.player = self.game_room.player_set.all()[0]
        self.assertTrue(self.namespace.on_leave_game())
        self.assertEqual(Player.objects.all().count(), 0)
        self.assertEqual(GameRoom.objects.all().count(), 0)
        self.namespace.emit.assert_called_with('leave_game')

    def test_on_start(self):
        """
        Make sure that the socket can start a game.
        """

        state = {"foo": "bar"}
        self.namespace.runner.get_state.return_value = state

        self.namespace.on_start()
        self.namespace.emit_to_room.assert_called_with(self.namespace.room,
                                                       'state', state)
