var current_player_id = null;

function changeCurrentPlayerId(new_player_id, alertMsg) {
    current_player_id = new_player_id;
    if (alertMsg) tellCurrentPlayer(alertMsg);
}

function gameIdToPlayerOrderId(game_id) {
  var ordered_game_ids = [my_game_id].concat(
    _.filter(player_ids, function(pid) { return pid > my_game_id; })).concat(
    _.filter(player_ids, function(pid) { return pid < my_game_id; }));
  return ordered_game_ids.indexOf(game_id) + 1;
}

function addCardsToStagingArea(cards) {
    _.each(cards, function(card) {
        card.class = "card";
        card.id = "card" + card.game_id;
        addCard(card, "staging_area");
    });
}

function addCardsToProperZones(zones) {
    var zone_id, s;
    _.each(zones, function(zone) {
        s = (zone.owner == null) ? "" : gameIdToPlayerOrderId(zone.owner);
        $("#" + zone.name + s).attr("id", "zone" + zone.game_id);
        _.each(zone.cards, function(card) {
            moveCard("card" + card, "zone" + zone.game_id, 0);
        });
    });
}

function setupInitialState(data) {
    addCardsToStagingArea(data.cards);
    addCardsToProperZones(data.zones);
}

function setupClickEvents(obj) {
    _.each(_.pairs(obj), function(kv) {
        var s = kv[0];
        var f = kv[1];
        $(s).click(f);
    });
}


function createSidebar() {
    var sidebar = $('#sidebar');
    var sidebarPadding = $("#sidebar-padding");
    var gameWrapper = $('#game-wrapper');
    var chatBox = $('#chat-box');
    var chatInput = $('#chat-input');
    var header = $('#header');
    var button = $('#chat-btn')

    sidebar.css('width', Math.floor(gameWrapper.width() * .15) + 'px');

    // var chatBoxFirstTop = 20;

    sidebarPadding.css('height',(header.outerHeight()) + 'px');

    var sidebarWidth = sidebar.width();
    var sidebarHeight = sidebar.height();

    var offsetV = 10;

    var boxWidth = Math.floor(sidebarWidth * .95);
    var boxHeight = Math.floor(sidebarHeight * .65);
    var buttonHeight = Math.floor(sidebarHeight * .2);
    var inputHeight = sidebarHeight - boxHeight - offsetV * 3 - buttonHeight;

    // chatBox.css('width', boxWidth - 10);
    chatBox.css('height', boxHeight - $("#eventbox").height() - $("h3").height() - 10);

    // chatInput.css('width', boxWidth);
    chatInput.css('height', inputHeight);
}

$(document).ready(function() {
    setupSockets();
    
    $("#player-names-btn").click(function() {
        $("#player-names").fadeToggle();
    });

    $('#destroy-game-room').click(function(){
        socket.emit('destroy_game');
    });

    $('#leave-game-room').click(function(){
        socket.emit('leave_game');
    });

    $("#open-chat-btn").click(function () {
        $("#sidebar").toggle();
        createSidebar();
    });

    $('#chat-input').keypress(function(input){
        console.log("Hi I'm here");
        if (input.keyCode == 13 && !input.shiftKey) {
            console.log("Now I'm here");
            $('#chat-btn').click();
        }
    })

    $('#chat-btn').click(function(){
        socket.emit('chat', {'msg': $('#chat-input').val(),
                            'sender': player_mapping[my_game_id] });
    });

    createSidebar();
    $(window).resize(createSidebar)

});
