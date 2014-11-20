// solitaire.js

// Make sure we register all callbacks
// card click function
$(".card").click(function() {
    if (!$(this).hasClass("selected")) {
        $(this).addClass("selected");
    } else if (selected == this) {
        $(this).removeClass("selected");
    } else {
        parent = $(this).parent();
        parent.click.apply(parent);
    }
    console.log(selected);
});

// zone click function
$(".zone").click(function() {
    if ($('.selected') != null && $(this).has($(selected)).length == 0) {
    	console.log("Request move " + $(selected).attr('name') + " to " + $(this).attr('name'));
        requestMoveCard($(selected).attr('id'), $(this).attr('id'));
    }
});

// deck click function
// shortcut to draw
$(".deck").click(function() {
    data = Object();
    data.action_name = 'draw';
    socket.emit('action', data);
    $(".selected").removeClass("selected")

});