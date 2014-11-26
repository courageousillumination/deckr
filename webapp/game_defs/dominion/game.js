var expecting_select = false;
var expecting_type = null;
var information_name = null;
var currently_selected = [];
var mouse_offset = 5;

function validateAddSelected(selected) {
    // Make sure it's of the right type
    return !(expecting_select === false ||
        !selected.hasClass(expecting_type.toLowerCase()))
}

function addSelected(selected) {
    var value, dict, index;
    if (!validateAddSelected(selected)) return;

    value = parseInt(selected.attr('id').substring(4));
    if (expecting_type != 'Cards') {
        dict = {'action_name': 'send_information'};
        dict[information_name] = value;
        socket.emit('action', dict);
    } else {
        // We have to deal with the list here
        index = currently_selected.indexOf(value);
        if (index > -1)
            currently_selected.splice(index, 1);
        else
            currently_selected.push(value);
    }
}

function supplyOnHover(e) {
    console.log("hover", this.id);
    var img, src, hover_id;
    hover_id = this.id + "-hover";
    // Create big image
    src = this.src;
    big_src = this.src.substring(0, src.length-4) + "-big.jpg";
    img = '<img id="'+hover_id+'" class="hover" src="'+big_src+'" />';
    $('body').append(img);
    $("#"+hover_id)
        .css("top", (e.pageY + mouse_offset) + "px")
        .css("left", (e.pageX + mouse_offset) + "px")
        .fadeIn("fast");
}

function supplyOnMouseMove(e) {
    var ele = $("#"+this.id+"-hover");
    var wH = $(window).height();
    var wW = $(window).width();
    var mY = e.pageY + mouse_offset;
    var mX = e.pageX + mouse_offset;
    if (mX > (wW/2)) {
        mX -= ele.width();
    }
    if (mY > (wH/2)) {
        mY -= ele.height();
    }
    ele.css("top", mY + "px").css("left", mX + "px");
}

function supplyOnMouseOut(e) {
    console.log("out");
    $("#"+this.id+"-hover").remove();
}

function supplyOnClick() {
    if (!expecting_select) {
        socket.emit('action', {
            'action_name': 'buy',
            'buy_zone': $(this).attr('id').substring(4)});
    } else {
        addSelected($(this));
    }
}

function cardOnClick() {
    if (!expecting_select) {
        socket.emit('action', {
            'action_name': 'play_card',
            'card': $(this).attr('id').substring(4)});
    } else {
        if ($(this).hasClass("selected")) {
            $(this).removeClass("selected");
        } else {
            $(this).addClass("selected");
        }
        addSelected($(this));
    }
}

function nextPhaseOnClick() {
    socket.emit('action', {'action_name': 'next_phase'});
}

function abandonShipOnClick() {
    socket.emit('abandon_ship');
}

function sendInfoOnClick() {
    var dict;
    dict = {'action_name': 'send_information'}
    dict[information_name] =  currently_selected;
    socket.emit('action', dict);
}

socket.on('state', function(data) {
    var click_fn_map = {
        ".card": cardOnClick,
        ".supply": supplyOnClick
    };
    setupInitialState(data);
    setupClickEvents(click_fn_map); 
    addBtn('Abandon Ship', 'abandon-ship-btn', abandonShipOnClick);
    addBtn('Send Info', 'send-info-btn', sendInfoOnClick);
    addBtn('Next Phase', 'next-phase-btn', nextPhaseOnClick);
    $('.supply img.card').hover(supplyOnHover, supplyOnMouseOut);
    $('.supply img.card').mousemove(supplyOnMouseMove);
});

socket.on('expected_action', function(data){
    var val, dict;
    if (data == null) {
        expecting_select = false;
        return;
    }
    if (data[0] == 'send_information') {
        expecting_select = true;
        information_name = data[1];
        expecting_type = data[2];
        currently_selected = [];

        if (expecting_type == "Bool" && my_game_id == data[3]) {
            val = confirm(data[4]);
            dict = {'action_name': 'send_information'}
            dict[information_name] =  val;
            socket.emit('action', dict);
        }
    }
});