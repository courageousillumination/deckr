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
	console.log('Moving ' + data.cardId + ' from ' + data.fromZoneId + ' to ' + data.toZoneId);
    moveCard(data.fromZoneId,
              data.toZoneId,
              data.cardId);
});

socket.on('remove_card', function(data) {
	/* Responds to remove_card message from server */
	console.log('Removing ' + data.cardId + ' from ' + data.zoneId);
	removeCard(data.zoneId, data.cardId);
});

socket.on('add_card', function(data) {
	/* Responds to add_card message from server */
	console.log('Adding new card to ' + data.zoneId);
	addCard(data.zoneId, data.cardDict);
})

/////////////////
// END SOCKETS //
/////////////////

/////////////////////
// BEGIN FUNCTIONS //
/////////////////////

function addCard(zoneId, cardDict) {
	/* Adds new card to a specified zone.
	   Generates element from cardDict.
	   We would ideally like to use jQuery data,
	   rather than attr. Would need an equivalent
	   to getElementById. */
	var zone = document.getElementById(zoneId);
	var newCard = document.createElement('img');
	if (!cardDict["id"]) {
		var err = "No id attribute provided with card."
		console.log(err)
		return err
	} else if (document.getElementById(cardDict["id"])) {
		var err = "Duplicate ad. Card already in play."
		console.log(err)
		return err
	}
	for (key in cardDict) {
		$(newCard).attr(key,cardDict[key]);
	}
	zone.appendChild(newCard);
}

function removeCard(zoneId, cardId) {
	/* Function to remove card. Currently unused. */
	zone = document.getElementById(zoneId);
	zone.removeChild(cardId);
}

function moveCard(fromZoneId, toZoneId, cardId) {
	/* Moves card from one zone to another, referenced by id.
	   SLIGHTLY BUGGY. AFAIK you should have to say:
	   fromZone.removeChild(card);
	   But you don't. The code works fine without it, 
	   and when you include it, the console randomly
	   throws "Node not found" errors on that line. */
	var card = document.getElementById(cardId);
	var fromZone = document.getElementById(fromZoneId);
	var toZone = document.getElementById(toZoneId);

	if (!toZone) {
		err = "Zone not found: " + toZoneId;
		console.log(err)
		return
	}

	selected = null;
	console.log("Selected nulled.");
	toZone.appendChild(card);
	
} 


function requestMoveCard(fromZoneId, toZoneId, cardId) {
	/* Sends card movement request to server */
	console.log("Sending move request to server.");
	socket.emit('make_action', {'cardId': cardId,
								'toZoneId': toZoneId,
								'fromZoneId': fromZoneId});
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
	addCard("playarea0",cardDict);	
	addCard("playarea0",cardDict2);	

	// zone click function
	$(".zone").click(function() {
	    if (selected != null && $(this).has($(selected)).length == 0) {
	    	console.log("Request move " + $(selected).attr('id'));
	        requestMoveCard($(selected).parent().attr('id'),
	       		$(this).attr('id'),
	       		$(selected).attr('id'));
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