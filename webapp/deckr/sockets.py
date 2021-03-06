"""
Stores all the socket logic for the deckr webapp.
"""

import traceback

from django.core.exceptions import ObjectDoesNotExist

from deckr.models import GameRoom, Player
from engine import game_runner
from socketio.mixins import BroadcastMixin, RoomsMixin
from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace


@namespace('/chat')
class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    """
    Represents simple socket logic for a Chat Room. Whenever it
    receives a chat event it will broadcast the data to the entire
    channel.
    """

    def on_chat(self, msg):
        """
        Called whenever the socket recieves a chat message. It
        will then broadcast the message to the rest of the channel.
        """

        self.broadcast_event('chat', msg)

# Used to store all the rooms. We use this instead of the RoomsMixin because
# it allows us to get state that's bulit into each GameNamespace (mainly the
# player).
ROOMS = {}


@namespace('/game')
class GameNamespace(BaseNamespace, BroadcastMixin):

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

    def emit_to_room(self, room, event, *args):
        """
        We override this so that it will actually broadcast to self.
        """

        for connection in ROOMS.get(room, []):
            connection.emit(event, *args)

    def on_start(self):
        """
        Starts the game. Can be called by any player.
        """

        if not self.runner.start_game(self.game_room.room_id):
            self.emit("error", "Not enough players have joined yet")
            return

        self.emit_to_room(self.room, 'start')

        trans = self.runner.get_public_transitions(self.game_room.room_id)
        state = self.runner.get_state(self.game_room.room_id,
                                      self.player.player_id)

        self.emit_to_room(
            self.room,
            'textbox_data',
            (self.player.nickname,
             trans,
             state))

    def recv_disconnect(self):
        """
        Make sure we explicitly call disconnect.
        """

        self.disconnect()

    def disconnect(self, silent=False):
        """
        Make sure when we disconnect that we remove ourselves from the room.
        """

        super(GameNamespace, self).disconnect(silent)
        if self.room is None:
            return

        ROOMS[self.room].remove(self)
        if len(ROOMS[self.room]) == 0:
            del ROOMS[self.room]

    def join_room(self, room):
        """
        This will add the current socket to the ROOMS list under the specified
        value.
        """

        self.room = room
        if ROOMS.get(room, None) is None:
            ROOMS[room] = set()
        ROOMS[room].add(self)

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
        self.join_room(room)
        self.player = player
        self.game_room = game_room
        self.emit('player_nick', {'nickname': player.nickname,
                                  'id': player.player_id})
        self.update_player_list()

        return True

    def update_player_list(self):
        """
        Broadcast names to room
        """

        if self.game_room is not None:
            player_names = [{'id': p.player_id, 'nickname': p.nickname}
                            for p in self.game_room.player_set.all()]
            self.emit_to_room(self.room, 'player_names', player_names)

    def on_action(self, data):
        """
        Called whenever the socket recieves a chat message. It
        will then broadcast the message to the rest of the channel.
        """

        # pylint: disable=W0142,bare-except
        # We want to make sure that a engine error doesn't kill the entire
        # socket. This is somewhat ugly, but hopefully we won't have engine
        # errors.

        # Stop spectators from doing anything
        if self.player is None:
            self.emit("error", "Spectators cannot make any moves")
            return False

        try:
            valid, msg = self.runner.make_action(self.game_room.room_id,
                                                 player=self.player.player_id,
                                                 **data)
        except:
            traceback.print_exc()
            self.emit("error", "Internal Server Error")
            return False

        if not valid:
            self.emit("error", msg)
            return False

        trans = self.runner.get_public_transitions(self.game_room.room_id)
        self.emit_to_room(self.room, 'state_transitions', trans)

        state = self.runner.get_state(self.game_room.room_id,
                                      self.player.player_id)
        self.emit_to_room(
            self.room,
            'textbox_data',
            (self.player.nickname,
             trans,
             state))

        # Get all the private transitions for all players
        for ns in ROOMS[self.room]:
            if ns.player is not None:
                trans = self.runner.get_player_transitions(ns.game_room.room_id,
                                                           ns.player.player_id)
                ns.emit('state_transitions', trans)

        # Broadcast what the Game is expecting
        expected = self.runner.get_expected_action(self.game_room.room_id)
        self.emit_to_room(self.room, 'expected_action', expected)

        return True

    def on_request_state(self):
        """
        The client will call this whenever they want the entire
        game state.
        """

        if self.game_room is None:
            self.emit("error", "Please connect to a game room first.")
            return False
        elif self.player is None:
            # Spectator is requesting state
            other_players = self.game_room.player_set.all()
            if len(other_players) > 0:
                state = self.runner.get_state(self.game_room.room_id,
                                              other_players[0].player_id)
            else:
                self.emit("error", "There are no actual players in the room.")
                return False
        else:
            state = self.runner.get_state(self.game_room.room_id,
                                          self.player.player_id)

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

        if self.game_room is None:
            self.emit("error", "Please connect to a game room first.")
            return False

        # Spectator is leaving
        if self.player is None:
            self.emit('leave_game')
        else:
            self.player.delete()
            self.update_player_list()
            self.emit('leave_game')

            if not self.game_room.player_set.all():
                self.game_room.delete()
                self.room = None
                self.game_room = None

            self.player = None

        return True

    def on_abandon_ship(self):
        """
        This should be called if there was an internal engine error and we
        want to flush the current state of the engine.
        """

        self.runner.abandon_ship(self.game_room.room_id)

    def on_chat(self, data):
        """
        Receive chat message from client.
        """

        self.emit_to_room(self.room, 'chat', data)

    def on_join_as_spectator(self, room):
        """
        This allows a socket connection for a spectator to view the game
        """

        try:
            game_room_id = int(room)
        except ValueError:
            self.emit("error", "Game room id is not an integer.")
            return False

        # Get the game room object
        try:
            game_room = GameRoom.objects.get(pk=int(game_room_id))
        except ObjectDoesNotExist:
            self.emit("error", "Can not find game room")
            return False

        self.join_room(room)
        self.player = None
        self.game_room = game_room
        return True

    def flush(self):
        """
        Clear out all internal state and trigger a disconnect. Should only be
        used for testing.
        """

        if self.player is not None:
            self.player.delete()

        self.disconnect()

        self.player = None
        self.game_room = None
        self.room = None
