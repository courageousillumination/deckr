// You could argue that this function is superfluous...
function addCard(cardDict, zoneId, place) {
    /* Adds new card to a specified zone.
       Generates element from cardDict.
       We would ideally like to use jQuery data,
       rather than attr. Would need an equivalent
       to getElementById. */
    var zone = document.getElementById(zoneId);
    if (zone == null) {return;}
    var siblings = zone.childNodes;
    var newCard = document.createElement('img');

    if (!cardDict["id"]) {
        var err = "No id attribute provided with card.";
        console.log(err);
        return err
    } else if (document.getElementById(cardDict["id"])) {
        var err = "Duplicate add. Card already in play.";
        console.log(err);
        return err;
    }
    $(newCard).attr('id', cardDict["id"]);
    // Should probably go into data
    $(newCard).attr('face_up', cardDict['face_up']);
    if (cardDict["face_up"]) {
        $(newCard).attr('src', "/static/deckr/cards/" + cardDict["front_face"]);
    } else {
        $(newCard).attr('src', "/static/deckr/cards/" + cardDict["back_face"]);
    }
    $(newCard).addClass('card');
    $(newCard).data("front_face", cardDict["front_face"]);
    $(newCard).data("back_face", cardDict["back_face"]);


    if (!place) {
        zone.appendChild(newCard);
    } else {
        if (place < siblings.length) {
                $('.selected').removeClass('selected');
                zone.insertBefore(newCard, siblings[siblings.length - place]);
        } else {
            var err = "Place does not exist."
            console.log(err);
            return err;
        }
    }
}


function moveCard(cardId, toZoneId, place) {
    /* Moves card from one zone to another, referenced by id.
       place is optional argument. Zero indexed, pops zero
       SLIGHTLY BUGGY. AFAIK you should have to say:
       fromZone.removeChild(card);
       But you don't. The code works fine without it,
       and when you include it, the console randomly
       throws "Node not found" errors on that line. */
    console.log("Moving card");
    console.log(cardId, toZoneId, place);
    var card = document.getElementById(cardId);
    var fromZone = card.parentElement;
    var toZone = document.getElementById(toZoneId);
    var siblings = toZone.children;

    //COMPATABILITY PROBLEM
    if ($(card).hasClass('card').length == 0) {
        var err = "Please don't misuse our functions. That is not a card.";
        console.log(err);
        return err;
    }

    if (!toZone) {
        err = "Zone not found: " + toZoneId;
        console.log(err);
        return;
    }

    if (!place) {
        $('.selected').removeClass('selected');
        toZone.appendChild(card);
    } else {
        if (place < siblings.length) {
                $('.selected').removeClass('selected');
                toZone.insertBefore(card, siblings[siblings.length - place]);
        } else {
            var err = "Place does not exist."
            console.log(err);
            return err;
        }
    }

}

// Requests should probably be their own functions.
// CHANGED: Removed fromZoneId from request!
function requestMoveCard(cardId, toZoneId) {
    /* Sends card movement request to server */
    console.log("Sending move request to server.");
    socket.emit('action', {'action_name': 'move_cards',
                           'card': cardId.substring(4),
                           'target_zone': toZoneId.substring(4)});
}

function gameOver(results) {
    /* Handles game_over */
    // Format of results is [(nick, won_or_lost, rank)]
    // except without the parens
}