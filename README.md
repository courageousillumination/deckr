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
  python manage.py runserver
```
  
At this point the server should be up and running at 127.0.0.1:8000. You can run unittests with 
```
python manage.py test 
```
and the integration tests with 
```
python manage.py harvest.
```
