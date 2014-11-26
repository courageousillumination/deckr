function addCardsToStagingArea(cards) {
    _.each(cards, function(card) {
        card.class = "card";
        card.id = "card" + card.game_id;
        addCard(card, "staging_area");
    });
}

function addCardsToProperZones(zones) {
    _.each(zones, function(zone) {
        var zone_id = zone.game_id;
        $("#" + zone.name).attr("id", "zone" + zone_id);
        _.each(zone.cards, function(card) {
            moveCard("card" + card, "zone" + zone_id, 0);
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
    $('#chat-box').css('top',($('#chat-box').offset().top + $('#header').outerHeight()) + 'px');
    $('#chat-box').css('width', $('#sidebar').width() - 20 + 'px');
});
