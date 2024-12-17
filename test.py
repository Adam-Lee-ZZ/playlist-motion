import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from lyricsgenius import Genius
from nltk.corpus import verbnet

token = '1Tt_Qe5YyldyFwOWpjIgfVDrmucxjTjCvjFjWY2lRHAA-nI5-XpaeJkjn9aLbXdM'
genius = Genius(access_token=token)
print(genius.search_song('Saturn',artist='SZA').lyrics)
