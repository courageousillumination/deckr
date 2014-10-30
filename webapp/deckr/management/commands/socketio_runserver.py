# source: https://github.com/iamjem/socketio_runserver
import atexit
import coverage

from optparse import make_option
from re import match
from thread import start_new_thread
from time import sleep
from os import getpid, kill, environ
from signal import SIGINT

from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import naiveip_re, DEFAULT_PORT
from django.utils import six
from django.utils.autoreload import code_changed, restart_with_reloader
from socketio.server import SocketIOServer


RELOAD = False
COVERAGE = None

def reload_watcher():
    global RELOAD
    while True:
        RELOAD = code_changed()
        if RELOAD:
            kill(getpid(), SIGINT)
        sleep(1)
        
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--noreload',
            action='store_false',
            dest='use_reloader',
            default=True,
            help='Do NOT use the auto-reloader.'),
        make_option(
            '--nostatic',
            action='store_false',
            dest='use_static_handler',
            default=True,
            help='Do NOT use staticfiles handler.'),
        make_option(
            '--enable-coverage',
            action='store_true',
            dest='enable_coverage',
            default=False,
            help='Enable coverage on specified modules.'),
    )
        
    def __init__(self):
        super(Command, self).__init__()
        
        self.addr = ''
        self.port = DEFAULT_PORT
        
    def handle(self, addrport='', *args, **options):
        if options.get('enable_coverage'):
            print "Enabling coverage for socketio server."
            coverage_omit = ['*/management/*',
                             '*/migrations/*']
                                    
            cov = coverage.coverage(source=['deckr'], 
                                    omit=coverage_omit,
                                    data_suffix = True)
            cov.start()
            
        if not addrport:
            self.addr = ''
            self.port = DEFAULT_PORT
            
        else:
            m = match(naiveip_re, addrport)
            if m is None:
                raise CommandError('"%s" is not a valid port number '
                                   'or address:port pair.' % addrport)
            self.addr, _, _, _, self.port = m.groups()

        environ['DJANGO_SOCKETIO_PORT'] = str(self.port)
        if options.get('use_reloader'):
            start_new_thread(reload_watcher, ())

        try:
            bind = (self.addr, int(self.port))
            print 'SocketIOServer running on %s:%s\n\n' % bind
            handler = get_handler(**options)
            server = SocketIOServer(
                bind, handler, resource='socket.io', policy_server=True)
            server.serve_forever()
        except KeyboardInterrupt:
            server.stop()
            if options.get('enable_coverage'):
                cov.stop()
                cov.save()
            if RELOAD:
                print 'Reloading...\n\n'
                restart_with_reloader()

def get_handler(**options):
    """
    Returns the django.contrib.staticfiles handler.
    """
    handler = WSGIHandler()
    try:
        from django.contrib.staticfiles.handlers import StaticFilesHandler
    except ImportError:
        return handler
    use_static_handler = options.get('use_static_handler')
    insecure_serving = options.get('insecure_serving', False)
    if (settings.DEBUG and use_static_handler or
            (use_static_handler and insecure_serving)):
        handler = StaticFilesHandler(handler)
    return handler
