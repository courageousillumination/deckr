var expecting_select = false;
var expecting_type = null;
var information_name = null;
var currently_selected = [];

function validateAddSelected(selected) {
    // Make sure it's of the right type
    return !(expecting_select === false ||
        !selected.hasClass(expecting_type.toLowerCase()))
}

function addSelected(selected) {
    var value, dict, index;
    if (!validateAddSelected(selected)) return;

    value = parseInt(selected.attr('id').substring(4));
    if (expecting_type != 'Cards') {
        dict = {'action_name': 'send_information'};
        dict[information_name] = value;
        socket.emit('action', dict);
    } else {
        // We have to deal with the list here
        index = currently_selected.indexOf(value);
        if (index > -1)
            currently_selected.splice(index, 1);
        else
            currently_selected.push(value);
    }
}

function supplyOnClick() {
    if (!expecting_select) {
        socket.emit('action', {
            'action_name': 'buy',
            'buy_zone': $(this).attr('id').substring(4)});
    } else {
        addSelected($(this));
    }
}

function cardOnClick() {
    if (!expecting_select) {
        socket.emit('action', {
            'action_name': 'play_card',
            'card': $(this).attr('id').substring(4)});
    } else {
        if ($(this).hasClass("selected")) {
            $(this).removeClass("selected");
        } else {
            $(this).addClass("selected");
        }
        addSelected($(this));
    }
}

function nextPhaseOnClick() {
    socket.emit('action', {'action_name': 'next_phase'});
}

function abandonShipOnClick() {
    socket.emit('abandon_ship');
}

function sendInfoOnClick() {
    var dict;
    dict = {'action_name': 'send_information'}
    dict[information_name] =  currently_selected;
    socket.emit('action', dict);
}

socket.on('state', function(data) {
    var click_fn_map = {
        ".card": cardOnClick,
        ".supply": supplyOnClick
    };
    setupInitialState(data);
    setupClickEvents(click_fn_map); 
    addBtn('Abandon Ship', 'abandon-ship-btn', abandonShipOnClick);
    addBtn('Send Info', 'send-info-btn', sendInfoOnClick);
    addBtn('Next Phase', 'next-phase-btn', nextPhaseOnClick);
});

socket.on('expected_action', function(data){
    var val, dict;
    if (data == null) {
        expecting_select = false;
        return;
    }
    if (data[0] == 'send_information') {
        expecting_select = true;
        information_name = data[1];
        expecting_type = data[2];
        currently_selected = [];

        if (expecting_type == "Bool" && my_game_id == data[3]) {
            val = confirm(data[4]);
            dict = {'action_name': 'send_information'}
            dict[information_name] =  val;
            socket.emit('action', dict);
        }
    }
});