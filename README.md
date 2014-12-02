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
these can be installed using your favorite package manager. If you are running Mac OSX and do not have Xcode installed, you will need to install it. You may need to use sudo when running pip install.

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

See the [Writing a Game Guide](https://github.com/courageousillumination/deckr/blob/documentation/docs/game_tutorial.md) for an intro to creating a game definition that can be uploaded to Deckr.

## What is Implemented

### First Iteration

### Webapp
* Feature: Game Room
  * Use Case: Create a game room
    * The player navigates to the "Select Game Type" page.
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
Hearts was our first multiplayer game. It shares the same cards with Solitaire, so it was relatively easy to implement. Hearts supports up to four players and the base rules can be found [here](http://www.bicyclecards.com/card-games/rule/hearts). Most of the rules of Hearts have been implemented with the exception of multiple rounds and passing.

#### Dominion
Dominion is a more complex card game involving 2 to 4 people. The base rules can be found [here](http://riograndegames.com/getFile.php?id=348) and the cards from the base set (all of which are implemented) can be found [here](http://dominionstrategy.com/card-lists/dominion-card-list/). This game illustrates additional complexity such as resolving cards, multi step actions, etc.

## Engine
We added in multiplayer functionality, namely the ability to remove players from games, as well as a way to track if an insufficient number of players was present (so the game could not start).  We were able to implement zones that belong to players, as well as a multiplicity of zones, which is a feature that greatly reduces the amount of repetition involved in setting up the zones by allowing us to specify types of zones that everyone has a certain number of.  We were able to create user_state_transitions, as these were absolutely required for multiplayer functionality. These transitions target specific players with specific transition information, rather than broadcasting the same transition to the entire room. We were also able to capture input from the UI and allow players to make required actions following other players. Finally, we were able to implement YAML definitions for cards.

## Webapp
We implemented spectators, who are able to request the state of the game from another player’s perspective and watch the movement of cards and zones. Spectators cannot start the game, end the game or make any card moves. Users can also upload game definitions to the server via the interface, and assuming that their code is valid, should be able to play the game they have designed. The form provides information about how each file functions and where to find example game definitions to copy their format.

## UI
We were able to allow players to leave the game while allowing other players to continue. Furthermore, the UI’s design was improved markedly in this iteration. It now includes an expandable/collapsible chatbox, a drop-down informing players of who else is in the game room, a feed detailing what actions have been made in the game, and in the case of Dominion, pop-up images of the cards and alt-text listing the cards’ features. We found that without an action feed and easily readable cards, usability was low, making these improvements necessary.