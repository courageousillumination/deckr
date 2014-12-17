function GameObject() {
  this.setter_callbacks = {};
}
GameObject.prototype.add_to_zone = function() { };
GameObject.prototype.set_value = function(name, value){
  this[name] = value;
  if (this.set_callbacks[name] != null) {
    this.set_callbacks[name].call(this);
  }
};

/* Include some basic GameObjects such as Players and Zones */

function GameO(game, dict) {
  this.game_id = dict.game_id;
  this.game = game;
}

GameO.prototype = new GameObject();

/* Zones */
function Zone(game, dict) {
  this.game_id = dict.game_id;
  this.game = game;
  this.owner = dict.owner;

  // Select the actual div associated with this Zone.

  // Check if we're owned by the game or by a specific player
  if (dict.owner !== 0) {
    // TODO: Per player zone logic here
  } else {
    expected_id = dict.name;
  }
  this.element = $("#" + expected_id);
  this.element.data('game_id', this.game_id);
  // Add all objects that belong to this zone.
  for (var i = 0; i < dict.objects.length; i++) {
    game.get_object(dict.objects[i]).add_to_zone(this);
  }
}

Zone.prototype = new GameObject();

/* Players */

function Player(game, dict) {
  this.game_id = dict.game_id;
  this.game = game;
}

Player.prototype = new GameObject();

var DECKR_OBJECT_MAPPING = {
  'Zone': Zone,
  'Player': Player,
  'Game': GameO
};

function create_game_object(game, dict) {
  /* Disptaches to the proper construct and returns that objects. */
  if (DECKR_OBJECT_MAPPING[dict.game_object_type] != null) {
    return new DECKR_OBJECT_MAPPING[dict.game_object_type](game, dict);
  } else {
    console.log("Got unexpected dictionary");
    console.log(dict);
  }
}
