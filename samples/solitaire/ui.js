var selected_card = null;
$(".card").onclick(function() {
    selected_card = this;
}

$(".zone").onclick(function() {
    if (selected_card != null) {
            do_action("move_card", {card: selected_card.data('game-id'),
                                    zone: this.data('game-id')});
    }
}