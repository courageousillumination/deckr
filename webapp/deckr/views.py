"""
Stores all the view logic for deckr.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.template import Template
from django.core.urlresolvers import reverse

from engine import game_runner

# We need to import the namespace so the URLs can be discovered.
from deckr.sockets import ChatNamespace  # pylint: disable=unused-import
from deckr.models import GameRoom, GameDefinition
from deckr.forms import CreateGameRoomForm


def index(request):
    """
    Simply return the index page without any context.
    """

    return render(request, "deckr/index.html", {'games': ['foo', 'bar']})


def test_game(request):
    sub_template = Template(open("../samples/testgame/layout.html").read())
    return render(request, "deckr/test_game.html",
                  {'sub_template': sub_template})

def test_solitaire(request):
    sub_template = Template(open("../samples/solitaire/layout.html").read())
    game = get_object_or_404(GameRoom, pk=game_room_id)

    return render(request, "deckr/test_solitaire.html",
                  {'sub_template': sub_template, 'game': game})

def game_room_staging_area(request):
    game = request.POST.get('game')
    return render(request, "deckr/game_room_staging_area.html", {'game': game})

def upload_new_game(request):
    return render(request, "deckr/upload_new_game.html", {})

def game_room(request, game_room_id):
    """
    This view will present the actual game room page for
    a given game_id.
    """

    game = get_object_or_404(GameRoom, pk=game_room_id)
    return render(request, "deckr/game_room_staging_area.html", {'game': game})

def create_game_room(request):
    """
    This will mainly present a CreateGameRoomForm and
    process that form when it is posted.
    """

    if request.method == "POST":
        form = CreateGameRoomForm(request.POST)
        if form.is_valid():
            # Create a game object in the engine
            path = form.cleaned_data['game_id'].path
            engine_id = game_runner.create_game(path)
            # Crate the GameRoom in the webapp
            room = GameRoom.objects.create(room_id=engine_id)

            # Redirect to the landing page for the room
            return redirect(reverse("deckr.game_room", args=(room.pk,)))
    else:
        form = CreateGameRoomForm()
    return render(request, "deckr/create_game_room.html",
                  {'form': form})
