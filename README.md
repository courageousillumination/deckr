#deckr

1. [Overview](#overview)
2. [Setup](#setup)
3. [Writing a Game](#writing-a-game)
4. [Playing a Game](#playing-a-game) 
5. [What is Implemented](#what-is-implemented)
6. [FAQ](#faq)

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

## Playing a Game

#### Creating a Game Room

To initiate a game, navigate to the home page (this can be found [here](http://deckr.mooo.com) for the live instance, or at localhost:8000 for your own instance). Select "Create New Game Room". From the dropdown, select the game you want to play, and click "Create Game Room". You will be taken to a screen where you can set a nickname for yourself. (If you would like to invite other players or spectators, copy the link at the bottom of the screen now.) Enter a name and click "Choose Nickname". You will be taken to the game room you created.

#### Beginning the Game

If you have selected a multiplayer game such as Hearts or Dominion, you will need to wait for other players to join before you may begin the game. To invite other players, simply send them the link you copied in the staging area. If you have lost this link, see the [FAQ](#faq). Once enough players have joined, anyone in the room may press "Start Game" to begin the game.

#### Joining a Game as a Player

Assuming the game has not started yet, navigate to the invite link provided to you by the player who created the game room. Enter a nickname here and press "Choose Nickname". You will be taken to the game room.

#### Joining a Game as a Spectator

You may join as a spectator whether or not a game has begun. To do so, navigate to the invite link provided by the person who created the game room. Without entering a nickname, press "Join as Spectator". You will be taken to the game room, but you will be unable to participate in the game. You may, however, participate in the chat.

#### Playing a Game

Once you have selected "Start Game", cards will be dealt to all the players. What happens next depends on the game.

##### Solitaire

To move a card, first click the card, then click where you would like to place the card. To move a stack of cards, click the highest card in the stack. For example, if you have a stack of cards 4♦-3♠︎-2♥︎, you should select the 4♦.

To flip over a card from the deck at the top left, click the deck. If all of the cards in the deck have been flipped, click the empty space where the deck was to restore it.

##### Hearts

Rules [here](http://www.bicyclecards.com/card-games/rule/hearts).

To play a card, click the card you would like to play, then click the large board in the center of the game. The game's action feed will notify you when it is your turn. It will also notify you when special actions need to be made.

To take the cards in the center when you win a trick, simply click the board in the center or any of the cards there. All cards will be awarded to you.

##### Dominion

Rules [here](http://riograndegames.com/getFile.php?id=348).
Card information [here](http://dominionstrategy.com/card-lists/dominion-card-list/).

When you start the game, a player will be selected to go first. The acion feed with indicate this, and the game will notify the player.

To end your current phase and move to the next phase, press the button at the top of the screen that reads either "Buy Phase" or "End Turn". 

Certain action cards require more information. This may be information from the player who has played the card (for instance, choosing a card to trash), from the other players (for instance, requiring them to discard or reveal cards), or from both. To resolve these cards, select the cards you would like to perform the action on, then press "Send Info" to tell the game that you have chosen. The game will wait until everyone has sent info, if necessary. The action feed with notify players when further action is required.

#### Chatting

To chat with other players, select the chat icon at the top right of the game room screen. Enter whatever you'd like to say into the bottom-most box, then press "Send Message".

## What is Implemented

### First Iteration

#### Webapp
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

#### Engine
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

### Games
In addition to the solitaire game we presented in the first iteration we implemented two new games in this iteration: Hearts and Dominion.

#### Hearts
Hearts was our first multiplayer game. It shares the same cards with Solitaire, so it was relatively easy to implement. Hearts supports up to four players and the base rules can be found [here](http://www.bicyclecards.com/card-games/rule/hearts). Most of the rules of Hearts have been implemented with the exception of multiple rounds and passing.

#### Dominion
Dominion is a more complex card game involving 2 to 4 people. The base rules can be found [here](http://riograndegames.com/getFile.php?id=348) and the cards from the base set (all of which are implemented) can be found [here](http://dominionstrategy.com/card-lists/dominion-card-list/). This game illustrates additional complexity such as resolving cards, multi step actions, etc.

### Engine
We added in multiplayer functionality, namely the ability to remove players from games, as well as a way to track if an insufficient number of players was present (so the game could not start).  We were able to implement zones that belong to players, as well as a multiplicity of zones, which is a feature that greatly reduces the amount of repetition involved in setting up the zones by allowing us to specify types of zones that everyone has a certain number of.  We were able to create user_state_transitions, as these were absolutely required for multiplayer functionality. These transitions target specific players with specific transition information, rather than broadcasting the same transition to the entire room. We were also able to capture input from the UI and allow players to make required actions following other players. Finally, we were able to implement YAML definitions for cards.

### Webapp
We implemented spectators, who are able to request the state of the game from another player’s perspective and watch the movement of cards and zones. Spectators cannot start the game, end the game or make any card moves. Users can also upload game definitions to the server via the interface, and assuming that their code is valid, should be able to play the game they have designed. The form provides information about how each file functions and where to find example game definitions to copy their format.

### UI
We were able to allow players to leave the game while allowing other players to continue. Furthermore, the UI’s design was improved markedly in this iteration. It now includes an expandable/collapsible chatbox, a drop-down informing players of who else is in the game room, a feed detailing what actions have been made in the game, and in the case of Dominion, pop-up images of the cards and alt-text listing the cards’ features. We found that without an action feed and easily readable cards, usability was low, making these improvements necessary.

## FAQ

##### Q: How do I get [package name]?

Make sure you have pip. To get pip, navigate [here](https://pip.pypa.io/en/latest/installing.html). Right-click the link to get-pip.py and save the target. In your shell, navigate to the folder where you downloaded the file and run

```
  python get-pip.py
```

Now you're ready to install other packages. To install one, simply run

```
  pip install [package-name]
```

You may need to use `sudo` to complete the install.
 
##### Q: `pip install [name]` isn't working.

**A:** Try running `sudo pip install [name]` instead. You might have to enter your password.

##### Q: I successfully installed everything, but later quit the shell. Which exact commands do I need to use to get the server running again?

**A:** Type the following into your shell:

```
  cd location_of_deckr_folder/deckr
  source venv/bin/activate
  cd webapp
```

From here you can run `make run`, `make test`, and so on.

##### Q: I'm trying to move a card, but it's not working!

**A:** You cannot drag the cards. To move a card, make sure you first clik the card, then click where you would like to go. Also be sure that you are making a legal action.

##### Q: I'm trying to start the game, but nothing happens when I press "start".

**A:** To play Hearts or Dominion, there must be at least one other player in the game.

##### Q: I forgot to copy the invite link. Can I get it back?

**A:** Yes! To figure out your invite link, simply look at the URL at the top of your game room. It should look something like

`(root_address)/game_room/(game_id_number)/?player_id=your_player_id`

 What you want is the game_id_number. The invite link that corresponds to your game_id_number is

`(root_address)/game_room_staging_area/(game_id_number)`

Simply replace (root_adress) with the address of the instance you are using (either deckr.mooo.com or localhost:8000) and replace (game_id_number) with the id number from your game room's URL. This is your invite link.

Alternatively, you could just use the "back" button, but if you've already begun the game and want to invite spectators, this is probably not a good idea.

##### Q: I'm playing Dominion, but I'm not sure how to resolve the action on (some action card).

A: Certain cards require that all of the players discard or reveal something or that you choose cards to discard. To resolve these actions, you need to use the "Send Info" button at the top of the page. Select the cards you want to perform the action on, then press "Send Info" to tell the game that these are the cards you want to use. In the case where all players need to perform an action, no one will be able to proceed until every player has selected cards and pressed "Send Info".

##### Q: Where is the chat?

**A:** At the top right of the game room screen, there is a picture of two chat bubbles. Clicking this will open the chat.

##### Q: Where is the chat?

**A:** Follow the directions above to open the chat. The action feed is displayed above the box where messages appear.

##### Q: How can I see who else is playing?

**A:** Next to the chat icon is some text that reads "Players", followed by the number of players. Clicking this will allow you to see the nicknames of the other players.

##### Q: The website layout looks a little bit off...

**A:** You might want to switch to Chrome.