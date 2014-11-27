var tricks = [];

function updateEventBoxAddTransition(transition, data, eventbox) {
    var zone_id, card_id, number, card_name;

    // IDs start at 0 in dictionary
    zone_id = transition[2] - 1;
    card_id = transition[1] - 1;
    switch(data.state.cards[card_id].number) {
        case 11: number = "jack"; break;
        case 12: number = "queen"; break;
        case 13: number = "king"; break;
        case 14: number = "ace"; break;
        default: number = data.state.cards[card_id].number.toString();
    }
    card_name = "the " + number + " of " + data.state.cards[card_id].suit;
    console.log(data.state.zones[zone_id].name);
    
    if(data.state.zones[zone_id].name == "play_zone")
        addToEventBox(eventbox, data.nickname + " played " + card_name + ".");
    if(data.state.zones[zone_id].name == "discard")
        tricks.push(card_name);
}

function updateEventBox(data) {
    var _data, tricks, eventbox, trick_text, trick_len;
    _data = getEventData(data);
    eventbox = document.getElementById("eventbox");
    tricks = [];

    console.log("parsing");
    _.each(_data.transitions, function(transition) {
        console.log("Cards: ", _data.state.cards);
        if (transition[0] === "add") {
            updateEventBoxAddTransition(transition, _data, eventbox);
        }
    });

    trick_len = tricks.length;
    if (trick_len > 0) {
        trick_text = nickname + " won ";
        _.each(tricks, function(card, i) {
            card += (i < trick_len) ? ", " : " and ";
            trick_text += card;
        });
        addToEventBox(eventbox, trick_text);
    }
    scrollEventBoxToBottom(eventbox);
}

function playZoneOnClick() {
    socket.emit('action', {'action_name': 'take_trick'});   
}

function deckOnClick() {
    data = Object();
    data.action_name = 'draw';
    socket.emit('action', data);
    unselectAll();
}

function cardOnClick() {
    socket.emit(
        'action',
        {'action_name': 'play_card',
         'card': $(this).attr('id').substring(4)
        });
}

function onTextboxData(data){
    console.log(data);
    updateEventBox(data);
}

socket.on('textbox_data', onTextboxData);

socket.on('state', function(data) {
    var click_fn_map = {
        ".deck": deckOnClick,
        ".card": cardOnClick,
        ".play_zone": playZoneOnClick
    };
    setupInitialState(data);
    setupClickEvents(click_fn_map);
    scrollEventBoxToBottom(document.getElementById("eventbox"))
});