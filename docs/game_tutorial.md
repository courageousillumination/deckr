Writing a Game Using Deckr
==========================

Introduction
------------
The goal of this document is to get you up and running writing games using
deckr. This tutorial assumes some basic knowledge of the programming/markup
languages used when creating a deckr game: Python, Javascript, YAML, HTML
and CSS. By the end of this tutorial we will have produced a mostly functioning
implementation of Hearts.

File structure overview
-----------------------

The first thing to understand about deckr is how files should be laid out. Your
deckr game should live in a single directory and contain the following files, everything except the
actual python file must follow the specified naming
convention.

- layout.html: This is a simple HTML file that defines where zones will exist in your game.
- game.css: This is a CSS stylesheet that will be included when running your game.
- game.js: Any javascript code that will be used to interact with your game should be included here.
- config.yml: This configuration file defines several aspects of the game.
- [game_name].py: This will contain all the back end rules that should be used to run your game.

Front End Files
---------------

deckr works through a web client, and one of the goals of deckr is to give the
developer full control over the enviornement. As such we allow you to specify how
your game will be laid out, and specify style sheets and javascript.

Writing the layout.html
~~~~~~~~~~~~~~~~~~~~~~~

The layout.html is a html fragment that defines how your game should be laid out.
In the hearts example the layout looks like this


    <div class="layout">
        <div class="table">
            <div class="row">
                <div class="zone stacked" id="discard3"></div>
                <div class="zone horizontal-fan facing-up hand" id="hand3"></div>
                <div class="zone stacked" id="discard4"></div>
            </div>

            <div class="row">
                <div class="vertical-fan facing-left zone hand" id="hand2"></div>

                <div class="center-field play_zone zone" id="play_zone"></div>

                <div class="vertical-fan facing-right zone hand" id="hand4"></div>
            </div>

            <div class="row">
                <div class="stacked zone" id="discard2"></div>
                <div class="horizontal-fan zone hand" id="hand1"></div>
                <div class="stacked zone" id="discard1"></div>
            </div>
            <div class="row">
                <div class="zone" id="side_zone"></div>
            </div>
        </div>
    </div>


There are couple things of interest here. First, is that the outer most layer
should be a div with class layout. What you do inside is mostly up to you. The
second thing of note is that these divs have a number of classes applied to them.
Most of the classes in this example (row, zone, stacked, horizontal/vertical fan) are defined
by deckr. Some (center-field) are defined by our custom CSS style sheet. Finally,
notice that all of the zones have ids. We will discuss zones more in depth when we
look at the config.yml, but let it suffice to say that in this case zone ids should
match up with the name specified in the configuration. The one exception is per
player zones. In this example, hand and discard are per player zones. These are
numbered from 1 to max players; each player will have the same perspective, with
player1 always being in the same position.


Backend Files
-------------

In addition to the frontend files, there are two main files that are needed
for the backend: the configuration and the game rules.

Writing your configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Configuration must be stored in a config.yml file. This file must contain at least a 'game_file', and a 'game_class' attribute. Here we will briefly explore
the possible options in a configuration file.

- game_file: This defines the python file where your main game definition lives. Do not include the .py.
- game_class: This defines the name of the class inside your python file that defines your game.
- max_players: The maximum number of players that can join the game.
- min_players: The minimum number of players required before the game can begin.
- zones: A list of zones that will be part of this game. Each zone must at least have a name. It can optionally have an owner, and a multiplicity.
  - owner: Set this to player if each player should have a copy of this zone. Good examples are hands, discards, decks, etc.
  - multiplicity: This is an integer indicating how many copies of a specific zone should be created. This is mainly a convenience method.
- card_set: This is a list of all cards that will be used in this game. Each card must at least have a name, a front_face image, and a back_face image. Any other values here will be set as attributes on the Card.

In our hearts game the configuration looks like this

```
---
game_file: "hearts"
game_class: "Hearts"
max_players: 4
min_players: 2
zones:
    - name: "hand"
      owner: "player"
    - name: "discard"
      owner: "player"
    - name: "play_zone"
    - name: "side_zone"
```

This shows us that the game can be found in the Hearts class in hearts.py, that it requiers 2 - 4 players, that ecah player has a hand and a discard, and that there is a shared play_zone and side_zone.

Writing the rules
~~~~~~~~~~~~~~~~~

Your game should live in a python class that inherits from Game deckr.engine.game. A Game is required to have a set_up, is_over, and winners function.

- set_up: This will be called when the game is started. The game will already have a list of players and zones. This step should create decks, set values, etc.
- is_over: This function must return a boolean and will be called at the end of every action to see if the game is over.
- winners: This function should return a list of player_ids for players that have won the game. This will only be called if is_over evaluates to True.

Once you have written these three functions your game will run but you will be unable to do anything. To make sure you can actually play the game we must add actions. Actions are created using the @action(restriction=...) decorator. restriction should be either None (if there are no restrictions) or a boolean test that takes the same arguments as the action and makes sure that the action is legal. For example, consider the play card action in hearts. We might write this action something like this.

```
def can_play_card(self, player, card):
  return self.current_player == player

@action(restriction=can_play_card)
  def play_card(self, player, card):
      player.hand.remove_card(card)
      self.play_zone.add_card(card)

      card.face_up = True
      if self.play_zone.suit is None:
          self.play_zone.suit = card.suit
```

After you've written all of the actions you're game is completed! You can test it out locally or upload it to our site and play with your friends.
