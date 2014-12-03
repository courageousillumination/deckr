// sockets.js

// Globals
var socket = io.connect("/game");
var player_mapping = {};
var player_ids = [];
var my_game_id = 0;

function setupSockets() {
    /* Sets up all socket events. */
    console.log('Setting up sockets.');
    var socket_fn_mapping = {
        'start': onStart,
        'add_card': onAddCard,
        'remove_card': onRemoveCard,
        'move_card': onMoveCard,
        'make_action': onMakeAction,
        'state_transitions': onStateTransitions,
        'leave_game': onLeaveGame,
        'game_over': onGameOver,
        'error': onGameError,
        'player_names': onPlayerNames,
        'player_nick': onPlayerNick,
        'chat': onChat
    };
    _.each(_.pairs(socket_fn_mapping), function (kv) {
        var event = kv[0];
        var fn = kv[1];
        socket.on(event, fn);
    });
}

function onStart() {
    /* Responds to start message from server */
    socket.emit('request_state');
    $("#start-btn").hide();
}

function onAddCard(data) {
    /* Responds to add_card message from server */
    addCard(data.cardDict, data.zoneId);
}

function onRemoveCard(data) {
    /* Responds to remove_card message from server */
    removeCard(data.zoneId, data.cardId);
}

function onMoveCard(data) {
    /* Responds to move_card message from server */
    moveCard(data.cardId, data.toZoneId);
}

function onMakeAction(data) {
    /* Responds to make_action actions */
    // MUST: Change this to be modular.
    if (data.action === 'move_card') {
        socket.emit('move_card', data);
    }
}

function onStateTransitions(data) {
    /* Responds to state_transitions message from server */
    _.each(data, performTransition);
}

function transitionAdd(transition) {
    /* Performs add state transition */
    moveCard("card" + transition[1], "zone" + transition[2]);
}

function transitionSet(transition) {
    /* Performs set state transition */
    
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
    /* Performs is_over transition */
    var winner = player_mapping[transition[1][0]];
    alert(winner + " won!");
}

function performTransition(t) {
    /* Performs the appropriate transition for t */
    var fn = t[0];
    var transition_fn_map = {
        'add': transitionAdd,
        'set': transitionSet,
        'is_over': transitionGameOver
    };
    if (_.has(transition_fn_map, fn)) transition_fn_map[fn](t);
}

function onLeaveGame(data) {
    /* Responds to leave_game message from server */
    window.location = '/';
}

function onGameOver(data) {
    /* Responds to a game_over message from server.*/
    console.log('Game over!');
    gameOver(data);
}

function onGameError(data) {
    /* Responds to error from server */
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
    /* Responds to list of players names from server
       and replaces player list dynamically */
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

function onPlayerNick(data) {
    /* Responds to player_nick message from server */
    my_game_id = data.id;
}

function onChat(data) {
    /* Responds to chat message from server */
    var sender = data.sender;
    var msg = data.msg;

    $('#chat-box').append('<div>'+'<span class="un">'+sender+'</span>'
                            + ': ' + msg+'</div>');
    $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);

    if (sender === player_mapping[my_game_id])
        $('#chat-input').val('');
}
