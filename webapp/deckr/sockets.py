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

        print "Got socket connection 1."

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

        print "Got socket connection 2."

    def on_start(self):
        """
        Starts the game. Can be called by any player.
        """

        self.runner.start_game(self.game_room.room_id)
        # Boadcast the state to all clients
        self.emit_to_room(self.room,
                          "state",
                          self.runner.get_state(self.game_room.room_id))

    def on_join(self, join_request):
        """
        Triggers when a client joins this room. Each room corresponds
        to a GameRoom object. If this gets a bad ID, or it fails
        to create it will return False and emit an error message.
        """

        room = join_request['game_room_id']
        player_id = join_request['player_id']

        try:
            game_room_id = int(room)
        except ValueError:
            self.emit("error", "Game room id is not an integer.")
            return False

        try:
            player_id = int(player_id)
        except ValueError:
            self.emit("error", "Player id is not an integer.")
            return False

        # Get the game room object
        try:
            game_room = GameRoom.objects.get(pk=int(game_room_id))
        except ObjectDoesNotExist:
            self.emit("error", "Can not find game room")
            return False

        try:
            player = Player.objects.get(pk=int(player_id))
        except ObjectDoesNotExist:
            self.emit("error", "Can not find player")
            return False

        # join the room
        self.player = player
        self.game_room = game_room
        self.room = room
        self.join(room)
        self.emit('player_nick', player.nickname)
        self.update_player_list()

        return True

    def update_player_list(self):
        """
        Broadcast names to room
        """

        if self.game_room is not None:
            player_names = [
                p.nickname for p in self.game_room.player_set.all()]
            self.emit_to_room(self.room, 'player_names', player_names)

    # This is extremely temporary.
    def on_move_card(self, data):
        """
        This should call the engine to determine if this is a valid move
        """
        self.emit('move_card', data)
        return True

    def on_action(self, data):
        """
        Called whenever the socket recieves a chat message. It
        will then broadcast the message to the rest of the channel.
        """

        print data

        error, transitions = self.runner.make_action(self.game_room.room_id,
                                                     **data)
        if error:
            self.emit("error", "Invalid move")
            return False

        print("Transitions", transitions)

        self.emit_to_room(self.room, 'state_transitions', transitions)
        return True

    def on_request_state(self):
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

    def on_update_nickname(self, nickname):
        """
        The client will call this when a player wants to change their nickname
        """

        if self.game_room is None or self.player is None:
            self.emit("error", "Please connect to a game room first.")
            return False

        old_nickname = self.player.nickname
        self.player.nickname = nickname
        try:
            self.player.save()
        except ValueError:
            self.emit("error", "Invalid nickname")
            self.player.nickname = old_nickname
            return False

        self.update_player_list()
        return True

    def on_destroy_game(self):
        """
        The client will call this when a player wants to end the game
        """

        if self.game_room is None or self.player is None:
            self.emit("error", "Please connect to a game room first.")
            return False

        for player in self.game_room.player_set.all():
            player.delete()

        self.game_room.delete()
        self.emit_to_room(self.room, 'leave_game')
        self.emit('leave_game')

        self.game_room = None
        self.player = None
        self.room = None

        return True

    def on_leave_game(self):
        """
        The client will call this when a player decides to leave
        """

        if self.game_room is None or self.player is None:
            self.emit("error", "Please connect to a game room first.")
            return False

        self.player.delete()
        self.update_player_list()
        self.emit('leave_game')

        if not self.game_room.player_set.all():
            self.game_room.delete()
            self.room = None
            self.game_room = None

        self.player = None
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
