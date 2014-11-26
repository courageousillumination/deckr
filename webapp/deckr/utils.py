"""
This module is for misc. utilites in deckr. This includes things like
what to do with an uploaded file, etc.
"""
from os.path import join as pjoin
from zipfile import ZipFile
import re

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

    game_file_name = re.sub('(?!^)([A-Z]+)', r'_\1', game_name).lower()
    required_files = [
        '__init__.py',
        'config.yml',
        'layout.html',
        game_file_name + '.py',
        'game.js',
        'game.css']
    files = zipped_file.namelist()
    folder = files[0]

    if all([(folder + f) in files for f in required_files]) and len(files) >= 6:
        zipped_file.extractall(path)
        zipped_file.close()
        return path
    else:
        raise ValueError('Zipped file fails to match expected structure')
