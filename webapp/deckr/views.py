"""
Stores all the view logic for deckr.
"""

from django.shortcuts import render
from django.template import Template

# We need to import the namespace so the URLs can be discovered.
from deckr.sockets import ChatNamespace  # pylint: disable=unused-import


def index(request):
    """
    Simply return the index page without any context.
    """

    return render(request, "deckr/index.html", {'games': ['foo', 'bar']})

def test_game(request):
	sub_template = Template(open("../samples/testgame/layout.html").read())
	return render(request, "deckr/test_game.html", 
				  {'sub_template': sub_template})

def game_room_staging_area(request):
	game = request.POST.get('game')
	return render(request, "deckr/game_room_staging_area.html", {'game': game})

def upload_new_game(request):
	return render(request, "deckr/upload_new_game.html", {})

def create_game_room(request):
    return render(request, "deckr/create_game_room.html",
                  {'games': ['Solitaire', 'TestGame']})
