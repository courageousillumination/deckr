function play_zone_on_click() {
  socket.make_action('take_trick', {});
}

function card_on_click() {
  // Doesn't mean anything to click on cards that are already in play.
  if (! $(this).parent().hasClass('hand')) {
    return;
  }
  socket.make_action('play_card', {card: $(this).data('game_id')});
}
game.add_callback('click', 'card', card_on_click);
game.add_callback('click', 'play_zone', play_zone_on_click);
