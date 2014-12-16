
function Card(game, dict) {
  this.game_id = dict.game_id;
  this.game = game;
  this.front_face = dict.front_face;
  this.back_face = dict.back_face;
  this.face_up = dict.face_up;

  // Create the image
  this.element = $(document.createElement('img'));
  this.element.addClass('card');
  this.update_face();

  this.set_callbacks = {'face_up': this.update_face};

}

Card.prototype = new GameObject();

Card.prototype.update_face = function() {
  src = this.face_up ? this.front_face : this.back_face;
  this.element.attr('src', '/static/deckr/cards/' + src);
};

Card.prototype.add_to_zone = function(zone) {
  zone.element.append(this.element);
};

DECKR_OBJECT_MAPPING.Card = Card;
