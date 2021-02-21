from typing import List

from spotipy.oauth2 import SpotifyOAuth
import spotipy

from ambiance.feature_engine.features import vectorize_features
from ambiance.keys import spotify
import ambiance.model.db as db
from ambiance.model.track import Track


def create_tracks(tracks: List[str]) -> List[Track]:
    # eventually going to get this from user_id -> oAuth dict
    sp = db.CLIENT_SPOTIPY
    sp.trace = True

    tracks = [track for track in tracks if track][:50]

    features = sorted((track for track in sp.audio_features(tracks) if track), key=lambda track: track["id"])
    track_info = sorted((track for track in sp.tracks(tracks)['tracks'] if track), key=lambda track: track["id"])

    return [vectorize_features(track, info) for track, info in zip(features, track_info)]



# demo
# print(get_tracks_features(['spotify:track:5TXDeTFVRVY7Cvt0Dw4vWW', 'spotify:track:2S2od3hT7ceytw7d1pTRuE']))
