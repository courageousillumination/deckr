from django.shortcuts import render

# We need to import the namespace so the URLs can be discovered.
from deckr.sockets import ChatNamespace  # pylint: disable=unused-import

def index(request):
    return render(request, "deckr/index.html", {})
