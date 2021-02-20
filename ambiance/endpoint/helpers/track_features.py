from typing import List

from spotipy.oauth2 import SpotifyOAuth
import spotipy

from ambiance.feature_engine.features import vectorize_features
from ambiance.model.track import Track


def create_tracks(tracks: List[str]) -> List[Track]:
    # eventually going to get this from user_id -> oAuth dict
    sp = spotipy.Spotify(
        oauth_manager=SpotifyOAuth())
    sp.trace = True

    features = sp.audio_features(tracks)

    feature_map = [vectorize_features(track, sp.track(track["id"])) for track in features]

    return feature_map


# demo
print(create_tracks(['spotify:track:5TXDeTFVRVY7Cvt0Dw4vWW', 'spotify:track:2S2od3hT7ceytw7d1pTRuE']))
