// index.js
// rename me!

/*var socket = io.connect("/chat");

socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});

socket.on('chat', function(data) {
    console.log(data);
});*/

function addCard(zoneId, cardDict) {
	var zone = document.getElementById(zoneId);
	var newCard = document.createElement('img');
	for (key in cardDict) {
		$(newCard).attr(key,cardDict[key]);
	}
	zone.appendChild(newCard);
}

function removeCard(zoneId, cardId) {
	zone = document.getElementById(zoneId);
	zone.removeChild(cardId);
}

function moveCard(fromZoneId, toZoneId, cardId, place) {
	var card = getElementById(cardId);
	var fromZone = getElementById(fromZoneId);
	var toZone = getElementById(toZoneId);

	toZone.appendChild()
} 

/*

socket.on('existing games', function(data) {
	var dropdown = document.getElementById("games-dropdown")
	var games = JSON && JSON.parse(data);
	while (dropdown.firstChild) {
		dropdown.removeChild(dropdown.firstChild);
	}
	var newelement;
	for (gameid in games) {
		newelement = document.createElement('option');
		newelement.appendChild(document.createTextNode(games[gameid]));
		newelement.setAttribute("name",gameid);
		dropdown.appendChild(newelement);
	}

});


*/