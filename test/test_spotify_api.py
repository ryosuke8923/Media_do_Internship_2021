import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)


CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CLIENT_CREDENTIALS_MANAGER = spotipy.oauth2.SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS_MANAGER)

def get_songs_from_playlist(playlist_id):
    result = spotify.playlist(playlist_id)
    if len(result) == 15:
        print("SUCCESS!")
    else:
        print("FAILED!")

if __name__ == '__main__':
    get_songs_from_playlist("6BGaNbk6J9JiPCjLAR3l3B")