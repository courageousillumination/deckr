var expecting_select = false;
var expecting_type = null;
var information_name = null;
var currently_selected = [];
var mouse_offset = 5;
var phase = "action";

function capitaliseFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function setupAltText(card) {
    if (card.face_up) {
        card.alt = "Name: " + card.name;
        card.alt += "\nType: " + capitaliseFirstLetter(card.card_type[0]);
        card.alt += "\nCost: " + card.cost + "\nEffect: " + card.effect;
    }
}

function findTransition(name, transitionList) {
  for(i=0; i<transitionList.length; i++) {
    if(transitionList[i].indexOf(name) > -1) {
      console.log("found");
      return i;
    }
  }

  return -1;
}

function parseAction(data) {

  nickname = data[0];
  transitions = data[1];
  state = data[2];

  textbox = document.getElementById("eventbox");

  // If there is a phase transitino, we can ignore other transitions
  if((index = findTransition("Phase",transitions)) > -1) {
    if(transitions[index][1] == "action") {
      // For action phase, we need to say whose turn it is
      next_player = document.getElementById("player-names").children[transitions[index][2]-1].innerHTML;
      
      textbox.innerHTML += "---------------------------&#13;";
      textbox.innerHTML += "It is " + next_player + "\'s turn.&#13;";
      textbox.innerHTML += "**Action Phase**&#13;";

      // Set the phase for later
      phase = "action";
     }
     else if(transitions[index][1] == "buy") {
      textbox.innerHTML += "**Buy Phase**&#13;";
      phase = "buy";
    }

    textbox.scrollTop = textbox.scrollHeight;
    return;
  }

  for(i = 0; i < transitions.length; i++) {
    transition = transitions[i];

    // This should be the only transition, if it exists
    if(transition[0] == "start") {
      // Find out who gets to play first
      starter = document.getElementById("player-names").children[transition[1]-1].innerHTML;

      textbox.innerHTML += nickname + " has begun the game.&#13;";
      textbox.innerHTML += "It is " + starter + "\'s turn.&#13;";
      textbox.innerHTML += "**Action Phase**&#13;"
    }

    if(transition[0] == "add") {
      card = transition[1] - 1;
      zone = transition[2] - 1;

      card_name = state.cards[card].name;

      if(phase == "action") {
        if(state.zones[zone].name == "play_zone") {
          textbox.innerHTML += nickname + " played a(n) " + card_name + ".&#13;";

          if(card_name == "Bureaucrat")
            textbox.innerHTML += "Waiting for players to reveal a victory card.";
          else if(card_name == "Militia")
            textbox.innerHTML += "Waiting for players to discard or counter-attack.";
          else if(card_name == "Spy")
            textbox.innerHTML += "Waiting for players to reveal a card.";
          else if(card_name == "Thief")
            textbox.innerHTML += "Waiting for players to reveal 2 treasure cards.";
          else if(card_name == "Witch")
            textbox.innerHTML += "Everyone gains 1 curse.";
          else if(card_name == "Council Room")
            textbox.innerHTML += "Everyone draws 1 card.";
        }
        else if(state.zones[zone].name == "trash") 
          textbox.innerHTML += nickname + " trashed a(n) " + card_name + ".&#13;";
        else if(state.zones[zone].name == "hand")
          textbox.innerHTML += nickname + " drew a card.&#13;";
        else if(state.zones[zone].name == "discard")
          textbox.innerHTML += nickname + " obtained a(n) " + card_name + ".&#13;";
      }
      else if(phase == "buy") {
        // Buying can involve multiple actions
        if(state.zones[zone].name == "play_zone")
          textbox.innerHTML += nickname + " played a " + card_name + ".&#13;";
        else if(state.zones[zone].name == "discard")
          textbox.innerHTML += nickname + " bought a(n) " + card_name + ".&#13;";
      }
    }
  }
  textbox.scrollTop = textbox.scrollHeight;
}

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
    var ele, wH, wW, mY, mX;
    ele = $("#"+this.id+"-hover");
    wH = $(window).innerHeight();
    wW = $(window).innerWidth();
    mY = e.pageY + mouse_offset;
    mX = e.pageX + mouse_offset;
    if (mX > (wW/2)) mX -= ele.width();
    if (mY > (wH/2)) mY -= ele.height();
    ele.css("top", mY + "px").css("left", mX + "px");
}

function supplyOnMouseOut(e) {
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

function onTextboxData(data){
    console.log(data);
    parseAction(data);
}

socket.on('textbox_data', onTextboxData);

socket.on('state', function(data) {
    var click_fn_map = {
        ".card": cardOnClick,
        ".supply": supplyOnClick
    };
    setupInitialState(data);
    _.each(data.cards, setupAltText);
    setupClickEvents(click_fn_map); 
    addBtn('Abandon Ship', 'abandon-ship-btn', abandonShipOnClick);
    addBtn('Send Info', 'send-info-btn', sendInfoOnClick);
    addBtn('Next Phase', 'next-phase-btn', nextPhaseOnClick);
    $('img.card').hover(supplyOnHover, supplyOnMouseOut);
    $('img.card').mousemove(supplyOnMouseMove);
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