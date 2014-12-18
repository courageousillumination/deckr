// sockets.js
// This has all functionality related to dealing with websockets and
// communication with the server.

function SocketWrapper(game, player_id) {
  // The socket wrapper provides a simple namespace for all socket
  // functionality.
  this.socket = null;
  this.game = game;

  this.initialize = function() {
    console.log('Setting up sockets.');

    // Connect the actual socket and join the game room.
    this.socket = io.connect("/game");
    this.socket.emit('join',  {game_room_id: game.game_id,
                               player_id: player_id});
    // Set up all callbacks
    var socket_fn_mapping = {
      'error': _.bind(this.on_error, this),
      'state': _.bind(this.on_state, this),
      'start': _.bind(this.on_start, this),
      'state_transitions': _.bind(this.on_state_transitions, this),

      /*'leave_game': this.onLeaveGame,
      'game_over': this.onGameOver,

      'player_names': this.onPlayerNames,
      'player_nick': this.onPlayerNick,
      'chat': this.onChat*/
    };


    var s = this.socket;
    _.each(_.pairs(socket_fn_mapping), function (kv) {
      var event = kv[0];
      var fn = kv[1];
      s.on(event, fn);
    });
  };

  this.start = function() {
    this.socket.emit('start');
  };

  this.request_state = function() {
    this.socket.emit('request_state');
  };

  this.make_action = function(name, extra_args) {
    if (extra_args === null) {
      extra_args = {};
    }
    extra_args.action_name = name;
    this.socket.emit('action', extra_args);
  };

  // Callbacks
  this.on_error = function(error_message) {
    console.log(error_message);
  };

  this.on_state = function(state) {
    // State will be a list of all game objects that currently exist.
    console.log("Recieved state from game: " + state.length + " objects.");
    this.game.create_game_objects(state);
  };

  this.on_start = function() {
    // When one player starts the game the game will send out a start message.
    // Generally all we need to do is request the current game state.
    console.log("Game has started, requesting state.");
    this.socket.emit('request_state');
  };

  this.on_state_transitions = function (transitions) {
    console.log("Applying " + transitions.length + " transitios");
    this.game.apply_transitions(transitions);
  };
}


/*
function onAddCard(data) {
      //console.log('Adding new card to ' + data.zoneId);
    addCard(data.cardDict, data.zoneId);
}

function onRemoveCard(data) {
    //console.log('Removing ' + data.cardId + ' from ' + data.zoneId);
    removeCard(data.zoneId, data.cardId);
}

function onMoveCard(data) {
    //console.log('Moving ' + data.cardId + ' to ' + data.toZoneId);
    moveCard(data.cardId, data.toZoneId);
}

function onMakeAction(data) {
    //console.log('Making action ' + data.action);
    // lol what...
    if (data.action === 'move_card') {
        socket.emit('move_card', data);
    }
}

function onStateTransitions(data) {
    _.each(data, performTransition);
}

function transitionAdd(transition) {
    moveCard("card" + transition[1], "zone" + transition[2]);
}

function transitionSet(transition) {
    // Could we make transition objects, instead of just magically knowing
    // which indices means what?

    // Set state
    // Check for flipping cards
    if (transition[1] == 'Card' && transition[3] == 'face_up') {
        card = $('#card' + transition[2]);
        if (transition[4]) {
            card.attr('src', card.data('front_face'));
            card.data('face_up', true);
        } else {
            card.attr('src', card.data('back_face'));
            card.data('face_up', false);
        }
    } else if (transition[1] === 'Player') {
        // something...
    }
}

function transitionGameOver(transition) {
    var winner = player_mapping[transition[1][0]];
    alert(winner + " won!");
}

function performTransition(t) {
    var fn = t[0];
    var transition_fn_map = {
        'add': transitionAdd,
        'set': transitionSet,
        'is_over': transitionGameOver
    };
    if (_.has(transition_fn_map, fn)) transition_fn_map[fn](t);
}

function onLeaveGame(data) {
    window.location = '/';
}

function onGameOver(data) {
    // Responds to a game_over message from server.
    console.log('Game over!');
    gameOver(data);
}

function onGameError(data) {
  // Responds to error from server
    console.log(data);
    // hoverError(data, {
    //     autoHide: false,
    //     clickOverlay: true,
    //     ShowOverlay: true,
    //     ColorOverlay: '#000',
    //     OpacityOverlay: 0.3,}
    // );
}

function onPlayerNames(players) {
    // Responds to list of players names from server and replaces player list dynamically
    innerHTML = "";
    player_ids = [];
    _.each(players, function(player) {
        innerHTML += '<li>' + player.nickname + '</li>';
        player_ids.push(player.id);
        player_mapping[player.id] = player.nickname;
    });
    $('#player-names').html(innerHTML);
    console.log($('#n-players'));
    $('#n-players').html(players.length);
}

function onPlayerNick(data){
    // $('#player_nick').html("Welcome " + data.nickname);
    my_game_id = data.id;
}

function onChat(data) {
    sender = data.sender ? data.sender : "Spectator";
    msg = data.msg;

    $('#chat-box').append('<div>'+'<span class="un">'+sender+'</span>'
                            + ': ' + msg+'</div>');
    $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);

    if (sender === player_mapping[my_game_id])  {
        $('#chat-input').val('');
    }
}*/
