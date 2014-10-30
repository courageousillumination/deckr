"""
Unit tests for deckr.
"""

from django.test import TestCase
from unittest import skip
from socketio.virtsocket import Socket
from mock import MagicMock

from deckr.sockets import *

class MockSocketIOServer(object):
    """
    Mock a SocketIO server
    """
    
    def __init__(self, *args, **kwargs):
        self.sockets = {}

    def get_socket(self, socket_id=''):
        return self.sockets.get(socket_id)


class MockSocket(Socket):
    pass

class ChatNamespaceTestCase(TestCase):
    """
    Test the ChatNamespace for websockets.
    """
    
    def setUp(self):
        self.server = MockSocketIOServer()
        self.environ = {}
        self.socket = MockSocket(self.server, {})
        self.socket.error = MagicMock()
        self.environ['socketio'] = self.socket
        self.namespace = ChatNamespace(self.environ, '/chat')
        self.namespace.broadcast_event = MagicMock()
        
    def test_chat(self):
        message = "hello world"
        
        self.namespace.on_chat(message)
        
        self.namespace.broadcast_event.assert_called_with("chat", message)
        
class GameNamespaceTestCase(TestCase):
    
    def setUp(self):
        self.server = MockSocketIOServer()
        self.environ = {}
        self.socket = MockSocket(self.server, {})
        self.socket.error = MagicMock()
        self.environ['socketio'] = self.socket
        self.namespace = GameNamespace(self.environ, '/game')
        self.namespace.broadcast_event = MagicMock()
        self.namespace.emit = MagicMock()
        
    @skip("Not yet implemented")
    def test_invalid_move(self):
        invalid_move = "invalid"
        self.namespace.on_action(invalid_move)
        
        self.namespace.emit.assert_called_with("error", "ERROR")
        
    @skip("Not yet implemented")
    def test_valid_move(self):
        valid_move = "valid move"
        transitions = "{ }"
        
        self.namespace.on_action(valid_move)
        
        self.namespace.broadcast_event.assert_called_with("state_transition",
                                                          transitions)
        
    @skip("Not yet implemented")
    def test_request_state(self):
        state = "{ }"
        
        self.namespace.on_request_state()
        
        self.namespace.emit.assert_called_with("state", state)
        