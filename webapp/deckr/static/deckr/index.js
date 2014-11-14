// index.js
// rename me!

// GLOBALS
var socket = io.connect("/game");
var selected = null;

////////////////////
// SOCKET SECTION //
////////////////////

socket.on('move_card', function(data) {
	/* Responds to move_card message from server */
	console.log('Moving ' + data.cardId + ' to ' + data.toZoneId);
    moveCard(data.cardId, data.toZoneId);
});

socket.on('remove_card', function(data) {
	/* Responds to remove_card message from server */
	console.log('Removing ' + data.cardId + ' from ' + data.zoneId);
	removeCard(data.zoneId, data.cardId);
});

socket.on('add_card', function(data) {
	/* Responds to add_card message from server */
	console.log('Adding new card to ' + data.zoneId);
	addCard(data.cardDict, data.zoneId);
});

socket.on('make_action', function(data) {
	/* Responds to make_action actions */
	console.log('Making action ' + data.action);
	if (data.action === 'move_card') {
		socket.emit('move_card', data);
	}
});

socket.on('state_transitions', function(data) {
    console.log(data);
    for (i = 0; i < data.length; i++) {
        // (name, args)
        // (add, card, zone)
        // (remove, card)
        // (set, type, id, name, value)
        transition = data[i];
        if (transition[0] == 'add') {
            moveCard("card" + transition[1], "zone" + transition[2]);
        }
        else if (transition[0] == 'set') {
            // Set state
            
            // Check for flipping cards
            if (transition[1] == 'Card' && transition[3] == 'face_up') {
                console.log("Setting card face up");
                cardId = '#card' + transition[2];
                console.log(cardId);
                console.log($(cardId));
                console.log($(cardId).data("front_face"));
                if (transition[4]) {
                    $(cardId).attr('src', "/static/deckr/cards/" + $(cardId).data('front_face'));
                    $(cardId).attr('face_up', 'true');
                } else {
                    $(cardId).attr('src', "/static/deckr/cards/" + $(cardId).data('back_face'));
                    $(cardId).attr('face_up', 'false');

                }
            }
        }
    }
});

socket.on('leave_game', function() {
	window.location = '/'

});

socket.on('game_over', function(data) {
	/* Responds to a game_over message from server.*/
	console.log('Game over!');
	gameOver(data);
});

socket.on('error', function(data) {
	/* Responds to error from server */
	console.log(data);
});

socket.on('player_names', function(names) {
	/* Responds to list of players names from server
     and replaces player list dynamically */
	var namesLength = names.length;
	innerHTML = ""
	for(var i = 0; i < namesLength; i++){
		 innerHTML += "<li>" + names[i] + "</li>";
	}
	$('#player_names').html(innerHTML);
})

socket.on('player_nick', function(nickname){
	$('#player_nick').html("Welcome " + nickname);
});

/////////////////
// END SOCKETS //
/////////////////

/////////////////////
// BEGIN FUNCTIONS //
/////////////////////

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

function addDiv(parentId, divDict, place) {
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
		$('.selected').removeClass('selected');
		parent.appendChild(newDiv);
	} else {
		if (place < siblings.length) {
				$('.selected').removeClass('selected');
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
		console.log(err)
		return
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

///////////////////
// END FUNCTIONS //
///////////////////

//////////////
// ON READY //
//////////////

$(document).ready(function() {

	$("#create-game-room #submit").click(function() {
		$("#create-game-room ").submit();
	});

	$('#destroy-game-room').click(function(){
		socket.emit('destroy_game');
	})

	$('#leave-game-room').click(function(){
		socket.emit('leave_game');
	})
})
