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

    sub_template = Template(open("../samples/solitaire/layout.html").read())

    return render(request, "deckr/index.html", {'games': ['foo', 'bar'], 'sub_template': sub_template})
    


