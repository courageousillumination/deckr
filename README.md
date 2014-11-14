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

 Pairs and Responsibilities
 -----

 Changes
 -----

 Miscellaneous
 -----