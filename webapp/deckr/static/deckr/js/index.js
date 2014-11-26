// index.js
$(document).ready(function() {
    $("form #submit.big-btn").click(function() {
        $(this).closest('form').submit();
    });

    $('#destroy-game-room').click(function(){
        socket.emit('destroy_game');
    });

    $('#leave-game-room').click(function(){
        socket.emit('leave_game');
    });
});
