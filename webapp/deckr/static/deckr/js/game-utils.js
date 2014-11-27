// game-utils.js

var jNotify_options = {
    autoHide: true,
    clickOverlay: true,
    MinWidth: 250,
    TimeShown: 3000,
    ShowTimeEffect: 200,
    HideTimeEffect: 200,
    LongTrip: 20,
    HorizontalPosition: 'center',
    VerticalPosition: 'top',
    ShowOverlay: false,
    ColorOverlay: '#000',
    OpacityOverlay: 0.3,
    onClosed: function(){},
    onCompleted: function(){}
};

function hoverError(message, opt) {
    opt = (!opt) ? jNotify_options : opt;
    jError(message, opt);
}

function hoverInfo(message, opt) {
    opt = (!opt) ? jNotify_options : opt;
    jNotify(message, opt);
}

function scrollEventBoxToBottom(eventbox) {
    eventbox.scrollTop = eventbox.scrollHeight;
}

function addToEventBox(eventbox, text, without_newline) {
    var n = (without_newline === true) ? "" : "&#13;";
    eventbox.innerHTML += text + n;
}

function getEventData(data) {
    return {
        nickname: data[0],
        transitions: data[1],
        state: data[2]
    };
}

function addBtn(label, btnId, fn) {
    if (!document.getElementById(btnId)) {
        $('#game-btns').append('<a href="#" id="'+btnId+'" class="small-btn"><div>'+label+'</div></a> ');
        if (fn) $('#'+btnId).click(fn);
    }
}

function changeBtnLabel(btnId, label) {
    $("#" + btnId + " div").html(label);
}

function unselectAll() {
    /* Unselects everything that is selected. */
    $('.selected').removeClass('selected');
}

function getZoneById(zoneId) {
    /* Gets element with id zoneId. If no such element exists,
       an error string is returned. */
    var zone, err;
    zone = document.getElementById(zoneId);
    // Validate zoneId
    if (zone == null) {
        err = "Zone not found: " + zoneId;
        console.log(err);
        return err;
    }
    return zone;
}

function invalidCardDict(cardDict) {
    /* Given a cardDict, returns false if the cardDict is valid
       (i.e. if the cardDict is not invalid). Otherwise, if the
       card dict is invalid, it returns an error string. */
    var err = false;
    if (!cardDict['id']) {
        err = "No id attribute provided with card."
        return err;
    } else if (document.getElementById(cardDict['id'])) {
        err = "Duplicate add. Card already in play.";
    }
    if (err) console.log(err);
    return err;
}

function createNewCard(cardDict) {
    /* Returns a img element for a given valid cardDict, populating
       data of the img element with data from the cardDict. If the
       cardDict is invalid, an error string is returned. */
    var err, newCard, k, v, src;
    // Validate cardDict
    err = invalidCardDict(cardDict);
    if (err) return err;

    newCard = document.createElement('img');
    $(newCard).attr('id', cardDict.id);
    $(newCard).attr('title', cardDict.alt);
    $(newCard).addClass('card');
    // Set newCard data based on cardDict
    _.each(_.pairs(cardDict), function(kv) {
        k = kv[0];
        v = kv[1];
        $(newCard).data(k, v);
    });
    src = cardDict.face_up ? cardDict.front_face : cardDict.back_face;
    $(newCard).attr('src', src);
    return newCard;
}

function addCard(cardDict, zoneId) {
    /* Given a valid cardDict and zoneId, creates a new card and adds
       it to the specified zone. If the cardDict or zoneId is invalid,
       an error string is returned. */
    //console.log("Adding card", cardDict, zoneId);
    var zone, newCard, err;
    zone = getZoneById(zoneId)
    if (_.isString(zone)) return zone;

    newCard = createNewCard(cardDict);
    if (_.isString(newCard)) return newCard;

    zone.appendChild(newCard);
}

function moveCard(cardId, toZoneId) {
    /* Moves card with id cardId to zone with id toZoneId. If the zoneId
       is invalid, an error string is returned. */
    //console.log("Moving card", cardId, toZoneId);
    var card, fromZone, toZone, err;
    card = document.getElementById(cardId);
    fromZone = card.parentElement;
    toZone = getZoneById(toZoneId);
    if (_.isString(toZone)) return toZone;

    unselectAll();
    toZone.appendChild(card);
}

function requestMoveCard(cardId, toZoneId) {
    /* Sends a request to the server to perform moveCard. */
    //console.log("Sending move request to server.");
    //console.log(cardId, cardId.substring(4));
    socket.emit('action', {'action_name': 'move_cards',
                           'card': cardId.substring(4),
                           'target_zone': toZoneId.substring(4)});
}

function gameOver(results) {
    /* Handles game_over */
}
