// index.js
// rename me!

var socket = io.connect("/chat");
socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});
socket.on('chat', function(data) {
    console.log(data);
});
socket.on('existing games', function(data) {

});