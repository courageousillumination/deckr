"""
Stores all the view logic for deckr.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.template import Template
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from engine import game_runner

# We need to import the namespace so the URLs can be discovered.
from deckr.sockets import ChatNamespace  # pylint: disable=unused-import
from deckr.models import GameRoom, Player
from deckr.forms import CreateGameRoomForm, PlayerForm


def index(request):
    """
    Simply return the index page without any context.
    """

    return render(request, "deckr/index.html", {'games': ['foo', 'bar']})


def test_game(request):
    """
    A test game page
    """
    sub_template = Template(open("../samples/testgame/layout.html").read())
    return render(request, "deckr/test_game.html",
                  {'sub_template': sub_template})


def game_room_staging_area(request, game_room_id):
    """
    This view will present the staging game room page for
    a given game_id.
    """

    game = get_object_or_404(GameRoom, pk=game_room_id)

    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.game_room = game
            player.player_id = game_runner.add_player(game.room_id)
            try:
                player.save()
                # Construct the get request for joining the game as
                # this player.
                url = (reverse("deckr.game_room", args=(game_room_id,)) +
                       "?player_id=" + str(player.pk))
                return redirect(url)
            except ValueError as e:
                # If there was an error saving the player we catch it and
                # add it as an error to the form.
                form.add_error('nickname', e.args[0])
    else:
        form = PlayerForm()

    return render(request,
                  "deckr/game_room_staging_area.html",
                  {'form': form,
                   'game': game})


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
            return redirect(
                reverse("deckr.game_room_staging_area", args=(room.pk,)))
    else:
        form = CreateGameRoomForm()

    return render(request, "deckr/create_game_room.html",
                  {'form': form})
