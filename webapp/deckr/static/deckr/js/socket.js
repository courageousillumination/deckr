// Globals
var player_mapping = {};
var player_ids = [];
var my_game_id = 0;

socket.on('start', function() {
    /* When the server says that we're starting we need to get the state. */
    socket.emit('request_state');
});

socket.on('move_card', function(data) {
    /* Responds to move_card message from server */
    console.log('Moving ' + data.cardId + ' to ' + data.toZoneId);
    moveCard(data.cardId, data.toZoneId);
});

socket.on('remove_card', function(data) {
    /* Responds to remove_card message from server */
    console.log('Removing ' + data.cardId + ' from ' + data.zoneId);
    removeCard(data.zoneId, data.cardId);
});

socket.on('add_card', function(data) {
    /* Responds to add_card message from server */
    console.log('Adding new card to ' + data.zoneId);
    addCard(data.cardDict, data.zoneId);
});

socket.on('make_action', function(data) {
    /* Responds to make_action actions */
    console.log('Making action ' + data.action);
    if (data.action === 'move_card') {
        socket.emit('move_card', data);
    }
});

socket.on('info_string', function(data) {
    $(eventbox).innerHTML += data;
});

socket.on('state_transitions', function(data) {
    console.log(data);
    for (i = 0; i < data.length; i++) {
        // (name, args)
        // (add, card, zone)
        // (remove, card)
        // (set, type, id, name, value)
        transition = data[i];
        if (transition[0] == 'add') {
            moveCard("card" + transition[1], "zone" + transition[2]);
        }
        else if (transition[0] == 'set') {
            // Set state

            // Check for flipping cards
            if (transition[1] == 'Card' && transition[3] == 'face_up') {
                console.log("Setting card face up");
                cardId = '#card' + transition[2];
                console.log(cardId);
                console.log($(cardId));
                console.log($(cardId).data("front_face"));
                if (transition[4]) {
                    $(cardId).attr('src', "/static/deckr/cards/" + $(cardId).data('front_face'));
                    $(cardId).attr('face_up', 'true');
                } else {
                    $(cardId).attr('src', "/static/deckr/cards/" + $(cardId).data('back_face'));
                    $(cardId).attr('face_up', 'false');

                }
            }
        } else if (transition[0] == 'is_over') {
            winner = player_mapping[transition[1][0]];
            alert("You won " +  winner);
        }
    }
});

socket.on('leave_game', function() {
    window.location = '/';

});

socket.on('game_over', function(data) {
    /* Responds to a game_over message from server.*/
    console.log('Game over!');
    gameOver(data);
});

socket.on('error', function(data) {
    /* Responds to error from server */
    console.log(data);
});

socket.on('player_names', function(players) {
    /* Responds to list of players names from server
     and replaces player list dynamically */

    var playersLength = players.length;
    innerHTML = "";
    player_ids = []
    for(var i = 0; i < playersLength; i++){
        innerHTML += "<li>" + players[i].nickname + "</li>";
        player_ids.push(players[i].id);
        player_mapping[players[i].id] = players[i].nickname;
    }

    $('#player_names').html(innerHTML);
});

socket.on('player_nick', function(data){
    $('#player_nick').html("Welcome " + data.nickname);
    my_game_id = data.id;
});
