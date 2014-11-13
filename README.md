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
	* Input**: Click "Create new game room". 
	* Output**: Transition to game creation screen.


2.
	* **Input**: Select nothing from the drop-down, then click "Create game room".
	* **Output**: A message stating that this field is required. 


3.	Input: Select "Solitaire" from the drop-down, then click "Create game room".
	Output: You will be taken to the "Set nickname" screen. It will read "Welcome to: Game room 0" at the top.

4. 	Input: Enter nothing into the text field and click "change name".
	Output: A message will appear stating that this field is required.

5.	Input: Enter a nickname into the text field.
	Output: You will be taken to an empty game room. You will see a message stating, "You are: [nickname]," followed by your nickname on the next line. The options to end the game, leave the game, or start are available.

6.	Input: Click start.
	Output: The game will be populated with cards, in the manner appropriate for solitaire.

7. 	Input: Click the deck.
	Output: A card will be flipped over next to the deck.

8.	Input: Place a card in front of another card (click first card, then the card you want to place it on).
	Output: If you have made a legal move, the card you selected first will move to where the second card is. If you have attempted to make an illegal move, nothing will happen.