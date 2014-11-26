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
});
