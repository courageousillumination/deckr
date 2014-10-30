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