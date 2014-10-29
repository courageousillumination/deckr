from subprocess import Popen, STDOUT
import os

from lettuce import *

@before.harvest
def run_server(variables):
    FNULL = open(os.devnull, 'w')
    
    world.server = Popen(["python", "manage.py", "socketio_runserver"],
                         stdout = FNULL, stderr = FNULL)
    
    print "Running socketio server at localhost:8000"

@after.harvest
def destroy_server(results):
    world.server.kill()