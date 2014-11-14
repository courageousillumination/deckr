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
    if (cardDict["face_up"]) {
        $(newCard).attr('src', "/static/deckr/cards/" + cardDict["front_face"]);
    } else {
        $(newCard).attr('src', "/static/deckr/cards/" + cardDict["back_face"]);
    }
    $(newCard).addClass('card');
    $(newCard).data("front_face", cardDict["front_face"]);
    $(newCard).data("back_face", cardDict["back_face"]);
    
    //TODO: Needs unit tests for place!
    if (!place) {
        zone.appendChild(newCard);
    } else {
        if (place < siblings.length) {
                selected = null;
                zone.insertBefore(newCard, siblings[siblings.length - place]);
        } else {
            var err = "Place does not exist."
            console.log(err);
            return err;
        }
    }
}

// TODO: Should combine aspects of addDiv and addCard...
//      to reduce code duplication.
function addDiv(divDict, parentId, place) {
    var parent = document.getElementById(parentId);
    var newDiv = document.createElement('div');
    var siblings = parent.childNodes;

    if (!divDict["id"]) {
        var err = "No id attr provided with div.";
        console.log(err);
        return err;
    } else if (document.getElementById(divDict["id"])) {
        var err = "Duplicate div. Div already exists.";
        console.log(err);
        return err;
    }
    for (key in divDict) {
        $(newDiv).attr(key,divDict[key]);
    }

    if (!place) {
        selected = null;
        parent.appendChild(newDiv);
    } else {
        if (place < siblings.length) {
                selected = null;
                toZone.insertBefore(newDiv, siblings[place]);
        } else {
            var err = "Place does not exist."
            console.log(err);
            return err;
        }
    }

}

function removeElementById(id) {
    /* Function to remove element. Currently unused. */
    element = document.getElementById(id);
    parent = element.parentElement;
    parent.removeChild(element);
}

function moveCard(cardId, toZoneId, place) {
    /* Moves card from one zone to another, referenced by id.
       place is optional argument. Zero indexed, pops zero
       SLIGHTLY BUGGY. AFAIK you should have to say:
       fromZone.removeChild(card);
       But you don't. The code works fine without it,
       and when you include it, the console randomly
       throws "Node not found" errors on that line.*/
    console.log("Moving card");
    console.log(cardId, toZoneId, place);
    var card = document.getElementById(cardId);
    var fromZone = card.parentElement;
    var toZone = document.getElementById(toZoneId);
    var siblings = toZone.children;

    //COMPATABILITY PROBLEM
    if (!$(card).hasClass('card')) {
        var err = "Please don't misuse our functions. That is not a card.";
        console.log(err);
        return err;
    }

    if (!toZone) {
        err = "Zone not found: " + toZoneId;
        console.log(err)
        return err
    }

    if (!place) {
        toZone.appendChild(card);
    } else {
        if (place < siblings.length) {
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
    socket.emit('action', {'action': 'move_card',
                           'card': cardId,
                           'target_zone': toZoneId});
}

function gameOver(results) {
    /* Handles game_over */
    // Format of results is [(nick, won_or_lost, rank)]
    // except without the parens
}