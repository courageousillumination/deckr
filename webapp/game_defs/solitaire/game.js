function zone_on_click() {
  if ($(this).attr('id') == 'deck') {
    socket.make_action('draw', {});
    $('.selected').removeClass('selected');
    return;
  }
  if ($('.selected').length !== 0 && $(this).has($('.selected')).length === 0) {
    socket.make_action('move_card', {card: $('.selected').data('game_id'),
                                     target_zone: $(this).data('game_id')});
    $('.selected').removeClass('selected');
  }
}
function card_on_click() {
  if ($('.selected').length === 0) {
    $(this).addClass('selected');
  } else if ($(this).hasClass('selected')) {
    $(this).removeClass('selected');
  } else {
    parent = $(this).parent();
    parent.click.apply(parent);
  }
}

function readjust_play_zones() {
  $(".play-zone").css("height", "auto");
  var maxH = _.max(_.map($(".play-zone"),
    function(e) { return $(e).height(); }
  ));
  var h = maxH + 75;
  $(".play-zone").css("height", h + "px");
}


game.add_callback('click', 'card', card_on_click);
game.add_callback('click', 'zone', zone_on_click);
game.set_post_state_change_callback(readjust_play_zones);
