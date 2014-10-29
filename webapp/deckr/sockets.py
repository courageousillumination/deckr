from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace


@namespace('/chat')
class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    def initialize(self):
        print "Got socket connection."

    def on_chat(self, msg):
        self.broadcast_event('chat', msg)
