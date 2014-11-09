// index.js
// rename me!

// GLOBALS
var socket = io.connect("/game");
var selected = null;

////////////////////
// SOCKET SECTION //
////////////////////
socket.on('connect', function() {
	socket.emit('join', game_id.toString());
});

// NOTE: Could probably replace lambdas with actual function calls.
socket.on('move_card', function(data) {
	/* Responds to move_card message from server */
	console.log('Moving ' + data.cardId + ' to ' + data.toZoneId);
    moveCard( data.cardId, data.toZoneId);
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

socket.on('game_over', function(data) {
	/* Responds to a game_over message from server.*/
	console.log('Game over!');
	gameOver(data);
})

socket.on('error', function(data) {
	/* Responds to error from server */
	console.log(data);
})

socket.on('player_names', function(data) {
	/* Responds to list of players names from server */
	console.log(data);
})

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
	for (key in cardDict) {
		$(newCard).attr(key,cardDict[key]);
	}
	
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
	   throws "Node not found" errors on that line. */
	var card = document.getElementById(cardId);
	var fromZone = card.parentElement;
	var toZone = document.getElementById(toZoneId);
	var siblings = toZone.children;

	//COMPATABILITY PROBLEM
	if (!card.classList.contains('card')) {
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
		selected = null;
		toZone.appendChild(card);
	} else {
		if (place < siblings.length) {
				selected = null;
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
	socket.emit('make_action', {'cardId': cardId,
								'toZoneId': toZoneId});
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
	/* Runs when document is ready. Includes the click handlers. */

	// Arbitrary definitions for testing.
	var cardDict = {"src" :"../static/deckr/cards/13.png", "id":"clubJack", "class":"card"};
	var cardDict2 = {"src" :"../static/deckr/cards/14.png", "id":"spadeJack", "class":"card"};
	addCard(cardDict, "playarea0");	
	addCard(cardDict2, "playarea0");	

	return;

	// zone click function
	$(".zone").click(function() {
	    if (selected != null && $(this).has($(selected)).length == 0) {
	    	console.log("Request move " + $(selected).attr('id'));
	        requestMoveCard($(selected).parent().attr('id'),
	       		$(this).attr('id'));
	    }
	});
	   
	// card click function
	$(".card").click(function() {
		if (!selected) {
	    	selected = this;
	    } else if (selected == this) {
	    	selected = null;
	    } else {
	    	parent = $(this).parent();
	    	parent.click.apply(parent);
	    }
	});

	$(window).unload(function(){
		socket.disconnect();
	});
})
