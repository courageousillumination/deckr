"""
Stores all the view logic for deckr.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.template import Template
from django.core.urlresolvers import reverse

from engine import game_runner

# We need to import the namespace so the URLs can be discovered.
from deckr.sockets import ChatNamespace  # pylint: disable=unused-import
from deckr.models import GameRoom, Player
from deckr.forms import CreateGameRoomForm


def index(request):
    """
    Simply return the index page without any context.
    """

    return render(request, "deckr/index.html", {'games': ['foo', 'bar']})

def game_room_staging_area(request, game_room_id):
    """
    This view will present the staging game room page for
    a given game_id.
    """

    game = get_object_or_404(GameRoom, pk=game_room_id)
    return render(request, "deckr/game_room_staging_area.html", {'game': game})

def game_room(request, game_room_id):
    """
    This view will present the actual game room page for
    a given game id
    """

    player_id = request.GET.get('player_id')
    player = get_object_or_404(Player, pk=player_id)
    game = get_object_or_404(GameRoom, pk=game_room_id)
    sub_template = Template(open("../samples/solitaire/layout.html").read())

    return render(request, "deckr/game_room.html",
                  {'sub_template': sub_template, 'game': game, 'player': player})

def upload_new_game(request):
    """
    Returns the view to upload a new game.
    """

    return render(request, "deckr/upload_new_game.html", {})

def create_game_room(request):
    """
    This will mainly present a CreateGameRoomForm and
    process that form when it is posted.
    """

    # pylint can't detect the constructor for a Django
    # form. So we disable the no-value-for-parameter here.
    # pylint: disable=no-value-for-parameter

    if request.method == "POST":
        form = CreateGameRoomForm(request.POST)
        if form.is_valid():
            # Create a game object in the engine
            path = form.cleaned_data['game_id'].path
            engine_id = game_runner.create_game(path)
            # Crate the GameRoom in the webapp
            room = GameRoom.objects.create(room_id=engine_id)

            # Redirect to the staging area for the room
            return redirect(reverse("deckr.game_room_staging_area", args=(room.pk,)))
    else:
        form = CreateGameRoomForm()
    return render(request, "deckr/create_game_room.html",
                  {'form': form})

def join_game_room(request):
    """
    Handles a player nickname submission.
    If valid nickname and there is space in the room, redirect to game room
    If valid nickname and there is NO space, redirect to spec room
    If invalid nickanme, render staging
    """

    game_id = int(request.POST.get('game_id'))
    try:
        game_room = GameRoom.objects.get(pk=int(game_id))
    except ObjectDoesNotExist:
        return False

    nickname = request.POST.get('nickname')

    try:
        player_id = game_runner.add_player(game_room.room_id)
        player = Player.objects.create(game_room=game_room,
                                   nickname=nickname,
                                   player_id=player_id)
    except ValueError:
        return False

    return redirect(reverse("deckr.game_room", args=(game_id,)))
