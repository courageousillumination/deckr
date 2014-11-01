// index.js
// rename me!

var socket = io.connect("/game");

socket.on('connect', function() {
    //socket.emit('my event', {data: 'I\'m connected!'});
});

/*socket.on('chat', function(data) {
    console.log(data);
});
*/

socket.on('move_card', function(data) {
	console.log('Moving ' + data.cardId + ' from ' + data.fromZoneId + ' to ' + data.toZoneId);
    moveCard(data.fromZoneId,
              data.toZoneId,
              data.cardId);
});

function addCard(zoneId, cardDict) {
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
	zone = document.getElementById(zoneId);
	zone.removeChild(cardId);
}

function moveCard(fromZoneId, toZoneId, cardId) {
	var card = document.getElementById(cardId);
	var fromZone = document.getElementById(fromZoneId);
	var toZone = document.getElementById(toZoneId);

	if (!toZone) {
		err = "Zone not found: " + toZoneId;
		console.log(err)
		return
	}

	//fromZone.removeChild(card);
	toZone.appendChild(card);
	selected = null;
} 

function requestMoveCard(fromZoneId, toZoneId, cardId) {
	console.log("Sending move request to server.");
	socket.emit('make_action', {'cardId': cardId,
								'toZoneId': toZoneId,
								'fromZoneId': fromZoneId});
}



var cardDict = {"src" :"static/deckr/cards/13.png", "id":"jack", "class":"card"};
var cardDict2 = {"src" :"static/deckr/cards/14.png", "id":"queen", "class":"card"};
var selected = null;

$(document).ready(function() {
	addCard("playarea0",cardDict);	
	addCard("playarea0",cardDict2);	

	// onclick function
	$(".zone").click(function() {
	    if (selected != null &&
	        $(this).has($(selected)).length == 0) {
	        	requestMoveCard($(selected).parent().attr('id'),
	        					$(this).attr('id'),
	        					$(selected).attr('id'));
	    }
	});
	   

	$(".card").click(function() {
		if (!selected) {
	    	selected = this;
	    } else if (selected == this) {
	    	selected = null;
	    } else {
	    	zone = $(this).parent();
	    	zone.click.apply(zone);
	    }
	});
})