from typing import List, Dict, Tuple

import numpy as np
from spotipy.oauth2 import SpotifyOAuth
import json
import spotipy

from ambiance.feature_engine.features import vectorize_features
from credentials import credentials


def get_tracks_features(tracks: List[str]) -> List[Tuple[str, np.ndarray]]:
    # eventually going to get this from user_id -> oAuth dict
    sp = spotipy.Spotify(
        client_credentials_manager=credentials)
    sp.trace = True

    features = sp.audio_features(tracks)

    feature_map = [vectorize_features(track) for track in features]

    return feature_map


# demo
# print(get_tracks_features(['spotify:track:5TXDeTFVRVY7Cvt0Dw4vWW', 'spotify:track:2S2od3hT7ceytw7d1pTRuE']))
