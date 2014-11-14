card-game-engine
================

A Card Game Engine for CMSC 22001


Setup
-----

After cloning the repository run the following commands:
```
  pip install virtualenv
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
  cd webapp
  make setup
  python manage.py socketio_runserver
```
  
At this point the server should be up and running at 127.0.0.1:8000. You can run unittests with 
```
python manage.py test 
```
and the integration tests (note you shouldn't be running the development server) with 
```
python manage.py harvest -S
```
The webapp also includes a Makefile that makes some general tasks easier. For
example `make verify` will run unittests, integration tests, and compile 
coverage information (all data will be written into a reports directory).
`make lint` will run pylint on the code base and generate a report. `make autolint`
will run autopep8 on the deckr code base to reduce pep8 violations.

Acceptance Tests
-----

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



What is Implemented
-----

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
We have not yet implemented the option to upload a game to the server.

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