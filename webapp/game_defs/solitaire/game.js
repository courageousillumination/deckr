// solitaire.js
function zoneOnClick() {
    if ($('.selected').length != 0 && $(this).has($('.selected')).length == 0) {
        console.log("Request move " + $('.selected').attr('id'));
        requestMoveCard($('.selected').attr('id'), $(this).attr('id'));
    }
}

function deckOnClick() {
    data = Object();
    data.action_name = 'draw';
    socket.emit('action', data);
    $('.selected').removeClass('selected');
}

function cardOnClick() {
    if($(this).attr('face_up') == 'false') {
        console.log('Clicked on face down card.');
        return
    }

    if ($('.selected').length == 0) {
        $(this).addClass('selected');
    } else if ($(this).hasClass('selected')) {
        $(this).removeClass('selected');
    } else {
        parent = $(this).parent();
        parent.click.apply(parent);
    }
    console.log($('.selected').attr('id') + " is selected.");
}

function readjustPlayZoneHeight() {
    $(".play-zone").css("height", "auto");
    var maxH = _.max(_.map($(".play-zone"), 
        function(e) { return $(e).height(); }
    ));
    var h = maxH + 75;
    $(".play-zone").css("height", h + "px");
}

socket.on('state', function(data) {
    var click_fn_map = {
        ".deck": deckOnClick,
        ".card": cardOnClick,
        ".zone": zoneOnClick
    };
    setupInitialState(data);
    setupClickEvents(click_fn_map);
    $('body').mousemove(readjustPlayZoneHeight);
});