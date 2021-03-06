"""
Stores all the view logic for deckr.
"""

# pylint can't detect the constructor for a Django
# form. So we disable the no-value-for-parameter here.
# pylint: disable=no-value-for-parameter

from os.path import join as pjoin

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import Template

from deckr.forms import (CreateGameRoomForm, PlayerForm,
                         UploadGameDefinitionForm)
from deckr.models import GameDefinition, GameRoom, Player
from deckr.sockets import ChatNamespace  # pylint: disable=unused-import
from deckr.utils import process_uploaded_file
from engine import game_runner
from zipfile import BadZipfile, LargeZipFile


def index(request):
    """
    Simply return the index page without any context.
    """

    return render(request, "deckr/index.html", {})


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
            try:
                player.player_id = game_runner.add_player(room.room_id)
                player.save()
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

    # Get Player info
    player_id = request.GET.get('player_id')
    if player_id is None:
        player = None
    else:
        player = get_object_or_404(Player, pk=player_id)

    game = get_object_or_404(GameRoom, pk=game_room_id)
    # Get GameDefinition info
    fin = open(pjoin(game.game_definition.path, 'layout.html')).read()
    js_file = open(pjoin(game.game_definition.path, 'game.js')).read()
    css_file = open(pjoin(game.game_definition.path, 'game.css')).read()
    sub_template = Template(fin)

    return render(request, "deckr/game_room.html",
                  {'sub_template': sub_template,
                   'game': game,
                   'game_js': js_file,
                   'game_css': css_file,
                   'player': player})


def upload_game_definition(request):
    """
    Returns the view to upload a new game.
    """
    if request.method == "POST":
        form = UploadGameDefinitionForm(request.POST, request.FILES)

        if form.is_valid():
            game_name = form.cleaned_data['game_name']
            try:
                GameDefinition.objects.get(name=game_name)
                form.add_error('game_name', "Game Definition already exists")
            except GameDefinition.DoesNotExist:
                try:
                    path = process_uploaded_file(game_name,
                                                 request.FILES['file'])
                    # Create a new GameDefinition
                    GameDefinition.objects.create(name=game_name,
                                                  path=path)
                    # Return to the index
                    return redirect(reverse('deckr.index'))
                # If there was an error with the file we catch it and
                # add it as an error to the form.
                except ValueError as exception:
                    form.add_error('file', exception.args[0])
                except BadZipfile as exception:
                    form.add_error('file', exception.args[0])
                except LargeZipFile as exception:
                    form.add_error('file', exception.args[0])

    else:
        form = UploadGameDefinitionForm()
    return render(request, "deckr/upload_game_definition.html", {'form': form})


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
            engine_id = game_runner.create_game(path)
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
