// index.js
// rename me!

// GLOBALS
var socket = io.connect("/game");
var selected = null;

////////////////////
// SOCKET SECTION //
////////////////////
socket.on('connect', function() {
    //socket.emit('my event', {data: 'I\'m connected!'});
});

/*socket.on('chat', function(data) {
    console.log(data);
});
*/


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
})

/////////////////
// END SOCKETS //
/////////////////

/////////////////////
// BEGIN FUNCTIONS //
/////////////////////

// You could argue that this function is superfluous...
function addCard(cardDict, zoneId) {
	/* Adds new card to a specified zone.
	   Generates element from cardDict.
	   We would ideally like to use jQuery data,
	   rather than attr. Would need an equivalent
	   to getElementById. */
	var zone = document.getElementById(zoneId);
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
	zone.appendChild(newCard);
}

function addDiv(parentId, divDict) {
	var parent = document.getElementById(parentId);
	var newDiv = document.createElement('div');
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
	parent.appendChild(newDiv);

}

function removeElementById(id) {
	/* Function to remove element. Currently unused. */
	element = document.getElementById(id);
	parent = element.parentElement;
	parent.removeChild(element);
}

function moveCard(cardId, toZoneId) {
	/* Moves card from one zone to another, referenced by id.
	   SLIGHTLY BUGGY. AFAIK you should have to say:
	   fromZone.removeChild(card);
	   But you don't. The code works fine without it, 
	   and when you include it, the console randomly
	   throws "Node not found" errors on that line. */
	var card = document.getElementById(cardId);
	var fromZone = card.parentElement;
	var toZone = document.getElementById(toZoneId);

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

	selected = null;
	toZone.appendChild(card);
	
} 

// Requests should probably be their own functions.
// CHANGED: Removed fromZoneId from request!
function requestMoveCard(cardId, toZoneId) {
	/* Sends card movement request to server */
	console.log("Sending move request to server.");
	socket.emit('make_action', {'cardId': cardId,
								'toZoneId': toZoneId});
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
	var cardDict = {"src" :"static/deckr/cards/13.png", "id":"clubJack", "class":"card"};
	var cardDict2 = {"src" :"static/deckr/cards/14.png", "id":"spadeJack", "class":"card"};
	addCard(cardDict, "playarea0");	
	addCard(cardDict2, "playarea0");	

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
})