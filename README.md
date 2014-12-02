#deckr

1. [Overview](#overview)
2. [Setup](#setup)
3. [Writing a Game](#writing-a-game)
5. [What is Implemented](#what-is-implemented)

## Overview

Deckr is a card game engine for [CMSC 22001](http://people.cs.uchicago.edu/~shanlu/teaching/22001_fa14/): Software Construction. The goal of this project is to create a reusable and extendable system for playing card games. Our system allows a user to define a card game using a combination of simple scripting and card definitions. Ideally our system will support many different types of card games from simple playing card games (Go Fish, War, Hearts) to complex trading card games (Magic: The Gathering, Pokemon, Yu-Gi-Oh!)

This application currently offers 3 games: Solitaire, Hearts, and Dominion.

## Setup

#### Prerequisites

To set up deckr you must have python 2.7, virtualenv, pip, and libevent. All of
these can be installed using your favorite package manager. If you are running Mac OSX and do not have Xcode installed, you will need to install it.

#### Installation

First clone the repository:
```
 git clone https://github.com/courageousillumination/deckr.git
```

After cloning the repository run the following commands:
```
  cd deckr
  pip install virtualenv
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
  cd webapp
  make setup
  make run
```

At this point the server should be up and running at localhost:8000.

The webapp also includes a Makefile that makes some general tasks easier.
* `make test` will run the unit tests
* `make verify` will run unit tests, integration tests, and compile coverage information (all data will be written into a reports directory)
* `make lint` will run pylint on the code base and generate a report.
* `make autolint` will run autopep8 on the deckr code base to reduce pep8 violations.


## Writing a Game

See the [Writing a Game guide](https://github.com/courageousillumination/deckr/blob/documentation/docs/game_tutorial.md) for an intro to create a game definition that can be uploaded to Deckr.

## What is Implemented

### First Iteration

### Webapp
* Feature: Game Room
  * Use Case: Create a game room
    * The player navigates to the select game type page.
    * The player selects the game he wants to play from a dropdown select field.
    * The player is able to set his nickname.
    * The player can start the game when ready.
* Feature: Game play
  * Use Case: User wants to interact with the game
    * The user makes an action through the UI, and the browser sends a websocket event to the server.
    * The server processes the event and determines if it is legal.
    * If the action is legal, the action is performed.


###Engine
* Feature: Define game
  * Use Case: Defining the game logic.
    * A developer writes a Python script (game.py) that interfaces with pre-defined functions to effect state changes in the card game.
  * Use Case: Defining the game ending
    * In game.py, the developer defines a function called “game_over(self)”.
    * At every state transition, the engine calls this function.
    * If the game should end, the function returns True.
    * If the game should not end, the function returns False.
  * Use Case: Defining the game set-up
    * In game.py, the developer defines a function called “set_up(self)”
    * This function will be called whenever the game begins.
    * The function generates the deck of cards (or analogous).
    * set_up populates all the zones of the table with cards.
    * set_up sets the initial states of all cards and creates a mapping from id’s to cards.
  * Use Case: Defining a new action
    * In game.py (or other file imported by game.py), the developer defines a new function with the @action decorator and checks the game state to ensure that the action is legal in the decorator.
    * The action makes any necessary state changes.
  * Use Case: An action is requested
    * The server transmits a requested action from the client.
    * The request includes a function name and arguments defined in game.py.
    * If legal, the game state calls the requested function, which makes necessary state changes.
    * If illegal, the engine catches an exception and informs the server the request was illegal.
* Feature: A pre-included definition of solitaire.
  * Use cases are as above in "webapp".

## Second Iteration

## Games
In addition to the solitaire game we presented in the first iteration we implemented two new games in this iteration: Hearts and Dominion.

#### Hearts
Hearts was our first multiplayer game. It shares the same cards with Solitaire, so it was relatively easy to implement. Hearts supports up to four players and the base rules can be found here. Most of the rules of Hearts have been implemented with the exception of multiple rounds and passing. Since Hearts is a simple game, and it was mainly intended to demonstrate our engine, we did not include unit tests for the game (similar to Solitaire).

#### Dominion
Dominion is a more complex card game involving 2 to 4 people. The base rules can be found here and the cards from the base set (all of which are implemented) can be found here. This game illustrates additional complexity such as resolving cards, multi step actions, etc. The complex nature of the game necessitated adding a number of features to the engine and a lot of testing, so we felt it was best to write some tests for this after all, although we at first did not expect this to be necessary. Still, this should not be considered a feature of the software itself so much as an example of the complex things the software can accomplish.

## Engine
We added in multiplayer functionality, namely the ability to remove players from games, as well as a way to track if an insufficient number of players was present (so the game could not start).  We were able to implement zones that belong to players, as well as a multiplicity of zones, which is a feature that greatly reduces the amount of repetition involved in setting up the zones by allowing us to specify types of zones that everyone has a certain number of.  We were able to create user_state_transitions, as these were absolutely required for multiplayer functionality. These transitions target specific players with specific transition information, rather than broadcasting the same transition to the entire room. We were also able to capture input from the UI and allow players to make required actions following other players. Finally, we were able to implement YAML definitions for cards.

## Webapp
We implemented spectators, who are able to request the state of the game from another player’s perspective and watch the movement of cards and zones. Spectators cannot start the game, end the game or make any card moves. Users can also upload game definitions to the server via the interface, and assuming that their code is valid, should be able to play the game they have designed. The form provides information about how each file functions and where to find example game definitions to copy their format.

## UI
We were able to allow players to leave the game while allowing other players to continue. Furthermore, the UI’s design was improved markedly in this iteration. It now includes an expandable/collapsible chatbox, a drop-down informing players of who else is in the game room, a feed detailing what actions have been made in the game, and in the case of Dominion, pop-up images of the cards and alt-text listing the cards’ features. We found that without an action feed and easily readable cards, usability was low, making these improvements necessary.

Card movement animation, while in our original design, was deemed not as necessary as having a working UI, so we did not implement it.  We also did not provide a toolkit for developers as it turned out to be too ambitious a goal.  


Pairs and Responsibilities
-----

(Looking at the git commit history gives a good enough idea, but considering that when working in pairs, only one person tends to commit code, this should clear up any uncertainty about who did what.)

* Tristan/Shaan: Built webserver.
* Alex/Graham: Wrote the website front-end. Wrote lettuce tests for front-end.
* Allison/Lee: Mapped out the components of cards, rules, etc. Wrote initial logic of Solitaire game. Implemented parts of the game engine (namely Zones, Regions, Cards)
* Joey/Hazel: Mapped out the functions the game engine would need. Implemented parts of the game engine (namely game, game_runner). Cleaned up/designed extra features for Solitaire. Wrote tests for solitaire [game] as well as socket tests and engine tests.
* Allison/Tristan: Web front-end touch-ups, refinements to Solitaire code. Wrote tests for parts of the game engine.
* Tristan: Major refinements/additions to game engine (game_object, game_runner, stateful_game_object, player, game)/solitaire code.



Changes
-----
The actual class structure of the game engine has diverged quite a bit from our original diagrams. We added game_objects to aid in associating ids with objects in play, and we added stateful_game_objects to provide a framework for tracking state transitions that objects undergo. These both serve as expedients for interfacing with the webapp, as they allow us to send information about an object's attributes (via dictionary) and its state transitions (via list) to the webapp. They also serve as helpful organizational abstractions for the game itself.

The functions within many of our extant classes (namely region, zone, game) have largely changed as well.

Cards no longer store type or id information explicitly; rather, these are created and set in the game's set_up function by appending attributes to the Card. This made more sense than using dictionaries to store information, as it was cleaner provided better ease of access (especially given how card structure can vary across non-playing card games). They are, however, aware of their zone.

Regions have an add_zone() function to expedite adding Zones to the Region properly.

We added peek(), push(), and pop() functions to Zones to help with ordered removal and addition of cards. A set_cards() function expedites adding a large number of cards to the zone.

The Game class now includes some helper classes, one for throwing exceptions, and the other allowing us to use @action wrappers to help with making game actions. The Game class itself now includes functions for getting and setting transitions (so we can track the game state and send it to the webabb), as well as a function to flush these transitions. Game objects can be found by id, and register() registers game objects to the game with a unique id. Configuration files specifiying different aspects of the game can also be loaded via load_config().

We added tests to Game and Game_Runner to cover new classes as well as to provide additional branch coverage.  We also changed some unit tests on the webserver to cover the fact that we are now getting additional data from the webserver (the player nicknames).

In general there were many edge cases which we didn't consider when writing our original batch of unittests. As we encountered these cases we
wrote additional unittests to test the cases. Currently we have around 95% line coverage and 90% branch coverage. Additionally, as we developed
and experimented with writing games we realized there were many things we could do to make our lives easier in the future; these were implemented
and had unittests created for them.
