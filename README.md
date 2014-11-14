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
  python manage.py migrate
  python manage.py socketio_runserver
```
  
At this point the server should be up and running at 127.0.0.1:8000. You can run unittests with 
```
python manage.py test 
```
and the integration tests with 
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
  * **Outout**: Game concludes and user may restart or return to the main page.

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

* Tristan/Shaan: Built webserver.
* Alex/Graham: Wrote the website front-end.
* Allison/Lee: Mapped out the components of cards, rules, etc. Wrote initial logic of Solitaire game. Implemented parts of the game engine (namely Zones, Regions, Cards)
* Joey/Hazel: Mapped out the functions the game engine would need. Implemented parts of the game engine (namely game, game_runner). Cleaned up/designed extra features for Solitaire.
* Allison/Tristan: Web front-end touch-ups, refinements to Solitaire code.
* Tristan: Major refinements/additions to game engine (game_object, game_runner, stateful_game_object, player, game)/solitaire code.



Changes
-----
 The actual class structure of the game engine has diverged quite a bit from our original diagrams. 