socket.on('state', function(data) {
    setupInitialState(data);

    // Super hacky. This should be cleaned up
    $(".card").click(function() {
      t = $(this);
      if (t.parent().hasClass('hand')) {
        socket.emit('action', {action_name: 'play_card', card: $(this).attr('id').slice(4)});
      }
      else {
        socket.emit('action', {action_name: 'activate_ability', card: $(this).attr('id').slice(4)});
      }
    });
});


function setValueCallback(transition) {
  console.log(transition);
  if (transition[0] == "set" && transition[1] == "Card" && transition[3] == "tapped") {
    $("#card" + transition[2]).data('tapped', transition[4]);
    if(transition[4]) {
      $("#card" + transition[2]).addClass('tapped');
    }
  }
}
