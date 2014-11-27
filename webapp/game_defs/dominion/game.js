var expecting_select = false;
var expecting_type = null;
var information_name = null;
var currently_selected = [];
var mouse_offset = 5;
var phase = "action";

function capitaliseFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function setPhase(new_phase) {
    phase = new_phase;
}

function addToEventBox(eventbox, text, without_newline) {
    var n = (without_newline === true) ? "" : "&#13;";
    eventbox.innerHTML += text + n;
}

function scrollEventBoxToBottom(eventbox) {
    eventbox.scrollTop = eventbox.scrollHeight;
}

function specialEventBoxCardText(card_name) {
    return {
        "Bureaucrat": "Waiting for players to reveal a victory card.",
        "Militia": "Waiting for players to discard or counter-attack.",
        "Spy": "Waiting for players to reveal a card.",
        "Thief": "Waiting for players to reveal 2 treasure cards.",
        "Witch": "Everyone gains 1 curse.",
        "Council Room": "Everyone draws 1 card."
    }[card_name];
}

function setupAltText(cardData) {
    var card = $("#card" + cardData.game_id);
    var alt = "";
    if (cardData.face_up) {
        alt += "Name: " + cardData.name;
        alt += "\nType: " + capitaliseFirstLetter(cardData.card_type[0]);
        alt += "\nCost: " + cardData.cost + "\nEffect: " + cardData.effect;
        card.attr("title", alt);
    }
}

function findTransition(name, transitions) {
    return _.findIndex(transitions, function(t) {
        return _.indexOf(t, name) > -1;
    });
}

function updateEventBoxPhaseTransition(transition, data, eventbox) {
    var i, next_player;
    if (transition[1] === "action") {
        i = transition[2]-1;
        next_player = document.getElementById("player-names").children[i].innerHTML;
        addToEventBox(eventbox, "---------------------------");
        addToEventBox(eventbox, "It is " + next_player + "\'s turn.");
        addToEventBox(eventbox, "**Action Phase**");
        if (my_game_id === i+1) hoverInfo("It is your turn!");

        // Set the phase for later
        setPhase("action");
    } else if (transition[1] === "buy") {
        addToEventBox(eventbox, "**Buy Phase**");
        setPhase("buy");
    }
}

function updateEventBoxStartTransition(transition, data, eventbox) {
    var i = transition[1]-1;
    var starter = document.getElementById("player-names").children[i].innerHTML;
    addToEventBox(eventbox, data.nickname + " has begun the game.");
    addToEventBox(eventbox, "It is " + starter + "\'s turn.");
    addToEventBox(eventbox, "**Action Phase**");
    if (my_game_id === i+1) hoverInfo("It is your turn!");
}

function updateEventBoxAddTransition(transition, data, eventbox) {
    var card, zone, card_name, state, verbs;
    state = data.state;
    card = transition[1] - 1;
    zone = transition[2] - 1;
    card_name = state.cards[card].name;
    zone_name = state.zones[zone].name;
    verb = {
        "play_zone": " player a ",
        "discard": " bought a(n) "
    }[zone_name];

    if (phase === "action")
        updateEventBoxAddActionTransition(transition, data, eventbox);
    else if (phase === "buy")
        addToEventBox(eventbox, data.nickname + verb + card_name + ".");
}

function updateEventBoxAddActionTransition(transition, data, eventbox) {
    var card, zone, card_name, state, verbs;
    state = data.state;
    card = transition[1] - 1;
    zone = transition[2] - 1;
    card_name = state.cards[card].name;
    zone_name = state.zones[zone].name;
    verb = {
        "trash": " trashed a(n) ",
        "hand": " drew a(n) ",
        "discard": " obtained a(n) "
    }[zone_name];
    
    if (zone_name == "hand") {
        addToEventBox(eventbox, data.nickname + " drew a card.");
    } else if (zone_name === "play_zone") {
        addToEventBox(eventbox, data.nickname + " played a(n) " + card_name + ".");
        addToEventBox(eventbox, specialEventBoxCardText(card_name));
    } else {
        addToEventBox(eventbox, data.nickname + verb + card_name + ".");
    }
}

function updateEventBox(data) {
    var eventbox, _data, transitions, i;
    eventbox = document.getElementById("eventbox");
    _data = {
        nickname: data[0],
        transitions: data[1],
        state: data[2]
    };
    transitions = {
        "start": updateEventBoxStartTransition,
        "add": updateEventBoxAddTransition
    };

    // If there is a phase transition, we can ignore other transitions
    i = findTransition("Phase", _data.transitions);
    if (i > -1) {
        updateEventBoxPhaseTransition(_data.transitions[i], _data, eventbox);
        scrollEventBoxToBottom(eventbox);
        return;
    }

    _.each(_data.transitions, function(transition) {
        if (_.has(transitions, transition[0]))
            transitions[transition[0]](transition, _data, eventbox);
    });
    scrollEventBoxToBottom(eventbox);
}

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

function supplyOnHover(e) {
    var img, src, hover_id;
    if (!$("#" + this.id).data("face_up")) return;
    hover_id = this.id + "-hover";
    // Create big image
    src = this.src;
    big_src = this.src.substring(0, src.length-4) + "-big.jpg";
    img = '<img id="'+hover_id+'" class="hover" src="'+big_src+'" />';
    $('body').append(img);
    $("#"+hover_id)
        .css("top", (e.pageY + mouse_offset) + "px")
        .css("left", (e.pageX + mouse_offset) + "px")
        .fadeIn("fast");
}

function supplyOnMouseMove(e) {
    var ele, wH, wW, mY, mX;
    ele = $("#"+this.id+"-hover");
    wH = $(window).innerHeight();
    wW = $(window).innerWidth();
    mY = e.pageY + mouse_offset;
    mX = e.pageX + mouse_offset;
    if (mX > (wW/2)) mX -= ele.width();
    if (mY > (wH/2)) mY -= ele.height();
    ele.css("top", mY + "px").css("left", mX + "px");
}

function supplyOnMouseOut(e) {
    $("#"+this.id+"-hover").remove();
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

function onTextboxData(data){
    console.log(data);
    updateEventBox(data);
}

socket.on('textbox_data', onTextboxData);

socket.on('state', function(data) {
    var click_fn_map = {
        ".card": cardOnClick,
        ".supply": supplyOnClick
    };
    setupInitialState(data);
    _.each(data.cards, setupAltText);
    setupClickEvents(click_fn_map); 
    addBtn('Abandon Ship', 'abandon-ship-btn', abandonShipOnClick);
    addBtn('Send Info', 'send-info-btn', sendInfoOnClick);
    addBtn('Next Phase', 'next-phase-btn', nextPhaseOnClick);
    $('img.card').hover(supplyOnHover, supplyOnMouseOut);
    $('img.card').mousemove(supplyOnMouseMove);
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