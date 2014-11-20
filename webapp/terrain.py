from subprocess import Popen
import signal
import os

from lettuce import after, world, before

@before.harvest
def run_server(_):
    FNULL = open(os.devnull, 'w')

    world.server = Popen(["python",
                          "manage.py",
                          "socketio_runserver",
                          "--noreload",
                          "--enable-coverage"],
                         stdout = FNULL, stderr = FNULL)

    print("Running socketio server at localhost:8000")

@after.harvest
def destroy_server(_):
    world.server.send_signal(signal.SIGINT)
    world.server.wait()
