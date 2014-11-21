"""
This module is for misc. utilites in deckr. This includes things like
what to do with an uploaded file, etc.
"""
from os.path import join as pjoin
from zipfile import ZipFile

from django.conf import settings


def process_uploaded_file(game_name, fin):
    """
    This will take in a zip file and unzip it to the game_defs directory. This
    will return the directory that we just unzipped to.
    """

    # Create a zipFile object
    zipped_file = ZipFile(fin)
    path_game_name = '_'.join(game_name.split()).lower()
    path = pjoin(settings.GAME_DEFINITION_PATH, path_game_name)
    # NOTE: This is gaping security hole. We've chosen not to deal with this
    #       problem in the project, but if this ever goes public we need to fix
    #       this.
    zipped_file.extractall(path)
    zipped_file.close()
    return path
