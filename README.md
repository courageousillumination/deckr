#deckr

1. [Overview](#overview)
2. [Setup](#setup)
3. [Writing a Game](#writing-a-game)
4. [Acceptance Tests](#acceptance-tests)
5. [What is Implemented](#what-is-implemented)

### Overview

Deckr is a card game engine for [CMSC 22001](http://people.cs.uchicago.edu/~shanlu/teaching/22001_fa14/) Software Construction. The goal of this project is to create a reusable and extendable system for playing card games. Our system allows a user to define a card game using a combination of simple scripting and card definitions. Ideally our system will support many different types of card games from simple playing card games (Go Fish, War, Hearts) to complex trading card games (Magic: The Gathering, Pokemon, Yu-Gi-Oh!)


### Prerequisites

To set up deckr you must have python 2.7, virtualenv, pip, and libevent. All of
these can be installed using your favorite package manager. If you are running Mac OSX and do not have Xcode installed, you will need to install it.

### Setup

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


###Writing a Game

See the [Writing a Game guide](https://github.com/courageousillumination/deckr/blob/documentation/docs/game_tutorial.md) for an intro to create a game definition that can be uploaded to Deckr.


###Acceptance Tests

######Test 1
  * **Input**: Click "Create new game room".
  * **Output**: Transition to game creation screen.

######Test 2
  * **Input**: Select nothing from the drop-down, then click "Create game room".
  * **Output**: A message stating that this field is required.

######Test 3
  * **Input**: Select "Solitaire" from drop-down. Click "Create game room".
  * **Output**: Transition to "Set Nickname" screen.

######Test 4
  * **Input**: Enter nothing into the text field. Click "change name".
  * **Output**: Message appears stating that this field is required.

######Test 5
  * **Input**: Enter a nickname into the text field.
  * **Output**: Transition to the game room.

######Test 6
  * **Input**: Click start.
  * **Output**: The game field is populated with cards in solitaire layout.

######Test 7
  * **Input**: Click the deck.
  * **Output**: A card is flipped over next to the deck.

######Test 8
  * **Input**: Click on a face-up card in the field of play.
  * **Output**: Yellow border appears around card.

######Test 9
 * **Input**: Click on another face-up card in the field of play.
 * **Output**: If move is legal, the card selected first moves to be in front of the card selected second. If move is illegal, nothing happens.

######Test 10
  * **Input**: Click an ace, then click the victory zone.
  * **Output**: Selected ace moves to the victory zone.

######Test 11
  * **Input**: Flip over cards in the deck until the deck is empty. Click empty deck space.
  * **Output**: Flipped cards return to the deck.

######Test 12
  * **Input**: Click a card that is flipped over.
  * **Output**: Nothing happens.

######Test 13
  * **Input**: Make moves until the game is won.
  * **Output**: Game concludes with a message notifying the user of victory.

######Test 14
  * **Input**: Click "End Game".
  * **Output**: Transition to main page.

######Test 15
  * **Input**: Click "Leave Game".
  * **Output**: Transition to main page.

#####Test Sequence 1 (Hearts Set-Up)
######Test 16
  * **Input**: Navigate to the main page, select “Create a Game Room”, and select “Hearts”. In another tab, copy the staging room link. Enter a username into the textbox on each tab (these must be different names; alternatively, find a friend to open the site on their own machine), and in each tab click “Choose Nickname”.
  * **Output**: You will be taken to a page with the Hearts game board.

######Test 17
  * **Input**: Select “start game”.
  * **Output**: In each tab, your hand will be populated with playing cards. The event feed (click the chat icon to view this) will display the nickname of the player who began the game.

######Test 18
  * **Input**: Click on the Two of Clubs in the hand of whichever player happens to hold it.
  * **Output**: The Two of Clubs will be moved from the player’s hand to the game board. The action feed will display the player’s nickname and state that you have played the Two of Clubs.

######Test 19
  * **Input**: Click on another card of the suit clubs in the hand of the player who did not play the first card.
  * **Output**: The card you click will move to the game board. The action feed will display the player’s nickname and state that you have played this card.

######Test 20
  * **Input**:  In the tab for whoever played the higher card (this will necessarily be the second player), click on one of the cards on the game board.
  * **Output**: All cards on the game board will move to that player’s discard pile.  The action feed will display the player’s nickname and state that you have won these cards.


#####Test Sequence 2 (Hearts Extras)
######Test 21
  * **Input**: Start a game of hearts as above, with as many players as you’d like. Have one of these players win the game.
  * **Output**: The game will announce that this player has won.
  Test Sequence 3 (Dominion Set-Up)

######Test 22
  * **Input**: Navigate to the main page, select “Create a Game Room”, and select “Dominion”. In another tab, copy the staging room link. Enter a username into the textbox on each tab (these must be different names; alternatively, find a friend to open the site on their own machine), and in each tab click “Choose Nickname”.
  * **Output**: You will be taken to a page with the Dominion game board.

######Test 23
  * **Input**: Select “start game”.
  * **Output**: The gameboard in each tab (or on each machine) will be populated with cards, as will your hand and deck. The action feed (click the chat icon to view this) will display the nickname of the player who began the game, the nickname of the player who goes first, and the current phase of the player’s turn (“action phase”).

######Test 24
  * **Input**: Select “next phase”.
  * **Output**: The action feed will display the game’s new phase (“buy phase”).

######Test 25
  * **Input**: Click on each treasure card in your hand. These are the gold cards with coins displayed on them.
  * **Output**: The treasure cards clicked will move to the play zone, the area directly above your hand.

######Test 26
  * **Input**: Click “next phase”.
  * **Output**: The action feed will display that it is now the other player’s turn and will note the current phase of their turn (“action phase”).

#####Test Sequence 4 (Dominion Extras)
######Test 27
  * **Input**: While in a game of Dominion, gain enough treasure to buy an Action card, buy the card, and play it when you next have a chance (this is when the Action card is in your hand and you are in Action Phase).
  * **Output**: The Action card will appear in your play zone. The action feed will state what card you have played.

######Test 28
  * **Input**: If the card necessitates discarding/trashing a card or choosing other players’ cards to take/discard/trash, select the cards you want and press “Send Info”. If other players must choose cards, the game will wait for them to do so.
  * **Output**: The actions performed by you and other players will be logged in the action feed.

######Test 29
  * **Input**: If the action card you played grants you more actions, you may choose to play another action card now.
  * **Output**: The effect of whatever action card you play will take place as outlined in the previous steps.

######Test 30
  * **Input**: If your action card gives you more coins, switch to buy phase, and attempt to buy something that requires these extra coins.
  * **Output**: You will buy the card.

######Test 31
  * **Input**: Win a game of Dominion.
  * **Output**: The game will announce that you have won.

#####Test Sequence 5 (Chat)
######Test 32
  * **Input**: While in a game, press the chat icon near the upper right hand corner.
  * **Output**: A sidebar with chat input and output boxes will appear on the right side of the screen.

######Test 33
  * **Input**: Type a message in the chat input box, press “Send Message.”
  * **Output**: Your message appears in the chat output box, with your username prepended. The same appears in all other users’ chat boxes, if they are displayed.
  Test Sequence 6 (Solitaire)

######Test 34
  * **Input**: Navigate to the main page, select “Create a Game Room”, and select “Solitaire.”Enter a username into the textbox.
  * **Output**: You are redirected to the game room.

######Test 35
  * **Input**: Press “Start.”
  * **Output**: The start button disappears, and a standard game of klondike solitaire is dealt.

######Test 36
  * **Input**: Select a card in the main play area.
  * **Output**: The card is highlighted in yellow.

######Test 37
  * **Input**: After selecting a card in the main play area, click on a card of the opposite color and one value point higher that is completely visible in the main area, not occluded (e.g. if you selected a red seven, click on a black eight, or if you selected a red ten, click on a black jack).
  * **Output**: The initially selected card moves on top of the clicked card, and no longer has its highlighting.

######Test 38
  * **Input**: Click on the deck (in the upper left corner of the table).
  * **Output**: A new card appears on the flipped deck. If that was the only card in the deck, then the deck is now empty.

#####Test Sequence 7 (Upload a game)
######Test 39
  * **Input**: Create a .zip archive containing the files described on the “Upload new game” page. Each of the files should follow the examples of the existing games.
  * **Output**: A new entry with the same name will appear on the “Create game room” dropdown menu. This game should play as expected.

#####Test Sequence 8 (Spectator)
######Test 40
  * **Input**: Create a game room for any game, and click “Join as Spectator”. You can choose to add real players to the game by copying the link at the bottom of the staging area to another tab, inputting a nickname, and pressing “Choose Nickname”.
  * **Output**: You will be taken to the game room, but you will not be able to perform any actions. Your nickname will be displayed as “Spectator”. Any actions made by the players in the room will be displayed to you in the same way it is displayed to them, but you will not see anyone’s hand.



##What is Implemented

###First Iteration

###Webapp
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

##Second Iteration

##Games
In addition to the solitaire game we presented in the first iteration we implemented two new games in this iteration: Hearts and Dominion.

####Hearts
Hearts was our first multiplayer game. It shares the same cards with Solitaire, so it was relatively easy to implement. Hearts supports up to four players and the base rules can be found here. Most of the rules of Hearts have been implemented with the exception of multiple rounds and passing. Since Hearts is a simple game, and it was mainly intended to demonstrate our engine, we did not include unit tests for the game (similar to Solitaire).

####Dominion
Dominion is a more complex card game involving 2 to 4 people. The base rules can be found here and the cards from the base set (all of which are implemented) can be found here. This game illustrates additional complexity such as resolving cards, multi step actions, etc. The complex nature of the game necessitated adding a number of features to the engine and a lot of testing, so we felt it was best to write some tests for this after all, although we at first did not expect this to be necessary. Still, this should not be considered a feature of the software itself so much as an example of the complex things the software can accomplish.

##Engine
We added in multiplayer functionality, namely the ability to remove players from games, as well as a way to track if an insufficient number of players was present (so the game could not start).  We were able to implement zones that belong to players, as well as a multiplicity of zones, which is a feature that greatly reduces the amount of repetition involved in setting up the zones by allowing us to specify types of zones that everyone has a certain number of.  We were able to create user_state_transitions, as these were absolutely required for multiplayer functionality. These transitions target specific players with specific transition information, rather than broadcasting the same transition to the entire room. We were also able to capture input from the UI and allow players to make required actions following other players. Finally, we were able to implement YAML definitions for cards.

##Webapp
We implemented spectators, who are able to request the state of the game from another player’s perspective and watch the movement of cards and zones. Spectators cannot start the game, end the game or make any card moves. Users can also upload game definitions to the server via the interface, and assuming that their code is valid, should be able to play the game they have designed. The form provides information about how each file functions and where to find example game definitions to copy their format.

##UI
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
