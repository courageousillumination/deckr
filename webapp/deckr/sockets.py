"""
Stores all the socket logic for the deckr webapp.
"""

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace


@namespace('/chat')
class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    """
    Represents simple socket logic for a Chat Room. Whenever it
    receives a chat event it will broadcast the data to the entire
    channel.
    """

    def initialize(self):
        """
        Mainly for debug.
        """

        print "Got socket connection."

    def on_chat(self, msg):
        """
        Called whenever the socket recieves a chat message. It
        will then broadcast the message to the rest of the channel.
        """

        self.broadcast_event('chat', msg)


@namespace('/game')
class GameNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    """
    Represents simple socket logic for a Chat Room. Whenever it
    recieves a chat event it will broadcast the data to the entire
    channel.
    """

    def initialize(self):
        """
        Mainly for debug.
        """

        print "Got socket connection."

    def on_make_action(self, data):
        """
        Called whenever the socket recieves a chat message. It
        will then broadcast the message to the rest of the channel.
        """
        
        print "Got socket data", data
        self.emit('move_card', data)
        #self.broadcast_event('chat', msg)