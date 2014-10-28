from django.shortcuts import render

from deckr.sockets import ChatNamespace

def index(request):
    return render(request, "deckr/index.html", {})