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

1.
  * **Input**: Click "Create new game room". 
  * **Output**: Transition to game creation screen.


2. 
  * **Input**: Select nothing from the drop-down, then click "Create game room".
  * **Output**: A message stating that this field is required. 


3. 
  * **Input**: Select "Solitaire" from drop-down. Click "Create game room".
  * **Output**: Transition to "Set Nickname" screen.

4. 
  * **Input**: Enter nothing into the text field. Click "change name".
  * **Output**: Message appears stating that this field is required.

5.
  * **Input**: Enter a nickname into the text field.
  * **Output**: Transition to the game room.

6. 
  * **Input**: Click start.
  * **Output**: Game field is populated with cards in solitaire layout.

7. 
  * **Input**: Click the deck.
  * **Output**: A card will be flipped over next to the deck.

8.
  * **Input**: Click on a face-up card in the field of play. 
  * **Output**: Yellow border appears around card.

9.
 * **Input**: Click on another face-up card in the field of play.
 * **Output**: If move is legal, the card selected first will move to mive in front of the second card. If move is illegal, nothing happens.