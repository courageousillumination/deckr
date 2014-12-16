function Game(game_id, player_id) {
  this.game_id = game_id;
  this.player_id = player_id;

  var players = [];
  var zones = [];
  var all_objects = {};
  var game = this;

  this.register = function(game_object) {
    all_objects[game_object.game_id] = game_object;
  };

  this.get_object = function(game_id) {
    return all_objects[game_id];
  };

  this.create_game_objects = function(all_objects) {
    // This will take in a list of dicts representing game objects and attempt
    // to actually make the game objects that these dicts are for.

    zone_objs = _.filter(all_objects, function(x) { return x.game_object_type == 'Zone';});
    player_objs = _.filter(all_objects, function(x) { return x.game_object_type == 'Player';});
    other = _.filter(all_objects, function(x) { return x.game_object_type !== 'Zone' && x.game_object_type !== 'Player';});
    // Set up players first. These shouldn't have and dependency on other objects
    players = _.map(player_objs, function(x) { return create_game_object(game, x);});
    _.map(players, this.register);

    // Set up all objects
    _.map(_.map(other, function(x) { return create_game_object(game, x);}), this.register);

    // We set up zones last, since other objects should be added to zones.
    zones = _.map(zone_objs, function(x) { return new Zone(game, x); });
    _.map(zones, this.register);
  };

  this.apply_transitions = function(transitions) {
    // Apply a set of transitions
    console.log(transitions);
    for (i = 0; i < transitions.length; i++) {
      transition = transitions[i];
      if (transition.name == 'add') {
        obj = this.get_object(transition.object);
        zone = this.get_object(transition.zone);
        obj.add_to_zone(zone);
      } else if (transition.name == 'remove'){
        // Currently a noop
      }
      else if (transition.name == 'set') {
        obj = this.get_object(transition.game_id);
        obj.set_value(transition.attribute, transition.value);
      }
      else {
        console.log("Got unexpected transition");
        console.log(transition);
      }
    }
  };
}
