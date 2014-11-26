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

function createSidebar() {
    var sidebar = $('#sidebar');
    var gameWrapper = $('#game-wrapper');
    var chatBox = $('#chat-box');
    var chatInput = $('#chat-input');
    var header = $('#header');
    var button = $('#chat-btn')

    sidebar.css('width', Math.floor(gameWrapper.width() * .15) + 'px')
    sidebar.css('height', '100%')

    chatBox.css('top',(chatBox.offset().top 
        + header.outerHeight()) + 'px');

    var sidebarWidth = sidebar.width();
    var sidebarHeight = sidebar.height();

    var offsetV = 10;

    var boxWidth = Math.floor(sidebarWidth * .95);
    var boxOffsetH = Math.floor((sidebarWidth - boxWidth) / 2);

    var boxHeight = Math.floor(sidebarHeight * .65);
    var buttonHeight = Math.floor(sidebarHeight * .2);
    var inputHeight = sidebarHeight - boxHeight - offsetV * 3 - buttonHeight;

    chatBox.css('left', boxOffsetH);
    chatBox.css('width', boxWidth);

    chatInput.css('left', boxOffsetH);
    chatInput.css('width', boxWidth);

    chatBox.css('height', boxHeight);
    chatInput.css('height', inputHeight);
    chatInput.css('top', chatBox.offset().top + boxHeight + offsetV)

    button.css('top', chatInput.offset().top + inputHeight + offsetV * 2);
    button.css('left', Math.floor((sidebarWidth - button.outerWidth()) / 2));
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

    createSidebar();

});
