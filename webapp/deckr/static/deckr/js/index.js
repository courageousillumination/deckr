// index.js

$(document).ready(function() {

    $("#create-game-room #submit").click(function() {
        $("#create-game-room ").submit();
    });

    $('#destroy-game-room').click(function(){
        socket.emit('destroy_game');
    });

    $('#leave-game-room').click(function(){
        socket.emit('leave_game');
    });
});
