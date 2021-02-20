from typing import List

from django.http import JsonResponse
from spotipy.oauth2 import SpotifyOAuth
import json
import spotipy


def get_tracks_features(tracks: List[str]) -> JsonResponse:
    # eventually going to get this from user_id -> oAuth dict
    sp = spotipy.Spotify(
        oauth_manager=SpotifyOAuth())
    sp.trace = True

    features = sp.audio_features(tracks)
    return json.dumps(features, indent=4)


# demo
print(get_tracks_features(['spotify:track:5TXDeTFVRVY7Cvt0Dw4vWW', 'spotify:track:2S2od3hT7ceytw7d1pTRuE']))
