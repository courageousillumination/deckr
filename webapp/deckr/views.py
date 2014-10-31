"""
Stores all the view logic for deckr.
"""

from django.shortcuts import render

# We need to import the namespace so the URLs can be discovered.
from deckr.sockets import ChatNamespace  # pylint: disable=unused-import

from xml.dom import minidom

DOC = minidom.parse("../../samples/solitaire/layout.html")

def index(request):
    """
    Simply return the index page without any context.
    """

    return render(request, "deckr/index.html", {})
    


