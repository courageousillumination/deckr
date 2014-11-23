"""
Stores all the view logic for deckr.
"""

# pylint can't detect the constructor for a Django
# form. So we disable the no-value-for-parameter here.
# pylint: disable=no-value-for-parameter

from os.path import join as pjoin

from django.shortcuts import render, redirect, get_object_or_404
from django.template import Template
from django.core.urlresolvers import reverse

from engine import game_runner

# We need to import the namespace so the URLs can be discovered.
from deckr.sockets import ChatNamespace  # pylint: disable=unused-import
from deckr.models import GameRoom, Player
from deckr.forms import CreateGameRoomForm, PlayerForm

GAME_RUNNER = game_runner


def set_game_runner(obj):
    """
    This is mainly for testing. But it could also be used
    to put in another game runner.
    """

    global GAME_RUNNER
    GAME_RUNNER = obj


def index(request):
    """
    Simply return the index page without any context.
    """

    return render(request, "deckr/index.html", {})


def test_game(request):
    """
    A test game page
    """
    sub_template = Template(open("game_defs/testgame/layout.html").read())
    return render(request, "deckr/test_game.html",
                  {'sub_template': sub_template})


def game_room_staging_area(request, game_room_id):
    """
    This view will present the staging game room page for
    a given game_id.
    """

    room = get_object_or_404(GameRoom, pk=game_room_id)

    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.game_room = room
            player.player_id = GAME_RUNNER.add_player(room.room_id)
            try:
                player.save()
                # Construct the get request for joining the game as
                # this player.
                url = (reverse("deckr.game_room", args=(game_room_id,)) +
                       "?player_id=" + str(player.pk))
                return redirect(url)
            except ValueError as exception:
                # If there was an error saving the player we catch it and
                # add it as an error to the form.
                form.add_error('nickname', exception.args[0])
    else:
        form = PlayerForm()

    return render(request,
                  "deckr/game_room_staging_area.html",
                  {'form': form,
                   'game_room': room})


def game_room(request, game_room_id):
    """
    This view will present the actual game room page for
    a given game id
    """

    player_id = request.GET.get('player_id')
    player = get_object_or_404(Player, pk=player_id)
    game = get_object_or_404(GameRoom, pk=game_room_id)
    fin = open(pjoin(game.game_definition.path, 'layout.html')).read()
    sub_template = Template(fin)

    return render(request, "deckr/game_room.html",
                  {'sub_template': sub_template,
                   'game': game,
                   'player': player})


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

    if request.method == "POST":
        form = CreateGameRoomForm(request.POST)
        if form.is_valid():
            # Create a game object in the engine
            game_def = form.cleaned_data['game_id']
            path = game_def.path
            engine_id = GAME_RUNNER.create_game(path)
            # Crate the GameRoom in the webapp
            room = GameRoom.objects.create(room_id=engine_id,
                                           game_definition=game_def)

            # Redirect to the staging area for the room
            return redirect(
                reverse("deckr.game_room_staging_area", args=(room.pk,)))
    else:
        form = CreateGameRoomForm()

    return render(request, "deckr/create_game_room.html",
                  {'form': form})
