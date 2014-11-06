"""
Stores all the socket logic for the deckr webapp.
"""

from django.core.exceptions import ObjectDoesNotExist

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace

from engine import game_runner

from deckr.models import Player, GameRoom


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
class GameNamespace(BaseNamespace, RoomsMixin):

    """
    Represents simple socket logic for a Chat Room. Whenever it
    recieves a chat event it will broadcast the data to the entire
    channel.
    """

    def __init__(self, *args, **kwargs):
        super(GameNamespace, self).__init__(*args, **kwargs)

        self.game_room = None
        self.player = None
        self.room = None
        self.runner = game_runner

    def initialize(self):
        """
        Mainly for debug.
        """

        print "Got socket connection."

    def recv_disconnect(self):
        """
        When we disconnect make sure we clean up any related
        objects.
        """

        if self.player is not None:
            self.player.delete()

    def on_join(self, room):
        """
        Triggers when a client joins this room. Each room corresponds
        to a GameRoom object. If this gets a bad ID, or it fails
        to create it will return False and emit an error message.
        """

        try:
            room_id = int(room)
        except ValueError:
            self.emit("error", "Room id is not an integer.")
            return False

        # Get the game room object
        try:
            game_room = GameRoom.objects.get(pk=int(room_id))
        except ObjectDoesNotExist:
            self.emit("error", "Can not find game room")
            return False

        # Attempt to create a player for this room
        try:
            player_id = self.runner.add_player(game_room.room_id)
            player = Player.objects.create(game_room=game_room,
                                           nickname="Bob",
                                           player_id=player_id)
        except ValueError:
            self.emit("error", "Unable to join game room.")
            return False

        # Now that we've created a player we can actually
        # join the room
        self.player = player
        self.game_room = game_room
        self.room = room
        self.join(room)

        return True

    def on_make_action(self, data):
        """
        Called whenever the socket recieves a chat message. It
        will then broadcast the message to the rest of the channel.
        """

        print "Got socket data", data
        self.emit('move_card', data)

    def on_request_state(self, data):
        """
        The client will call this whenever they want the entire
        game state.
        """

        if self.game_room is None:
            self.emit("error", "Please connect to a game room first.")
            return False

        state = self.runner.get_state(self.game_room.room_id)
        self.emit("state", state)
        return True

    def flush(self):
        """
        Clear out all internal state. Should only be used
        for testing.
        """

        if self.player is not None:
            self.player.delete()

        self.player = None
        self.game_room = None
        self.room = None
