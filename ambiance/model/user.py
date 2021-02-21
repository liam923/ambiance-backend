from dataclasses import dataclass, field

import spotipy
import numpy as np
from dataclasses_json import DataClassJsonMixin
from spotipy import Spotify
from typing import List, Set

from ambiance.helpers import top_tracks, track_features, saved_tracks, playlist_tracks
from ambiance.feature_engine.features import average_features
from ambiance.model.spotify_auth import Credentials
from ambiance.model.track import Track

import pendulum


@dataclass
class User(DataClassJsonMixin):
    id: str
    credentials: Credentials
    spotipy: Spotify = None
    library: Set[Track] = field(default_factory=set)

    saved_tracks: Set[Track] = field(default_factory=set)
    playlist_tracks: Set[Track] = field(default_factory=set)
    top_tracks: Set[Track] = field(default_factory=set)

    pref: np.ndarray = field(default_factory=lambda: np.array([]))

    def __post_init__(self):
        self.spotipy = spotipy.Spotify(client_credentials_manager=self.credentials)

    def update(self):
        # print(f"Saved tracks: {pendulum.now()}")
        saved_track_uris = saved_tracks.get_saved_tracks(self.id)
        # print(len(saved_track_uris))
        # print(f"Playlist tracks: {pendulum.now()}")
        playlist_track_uris = playlist_tracks.get_playlist_tracks(self.id)
        # print(f"Top tracks: {pendulum.now()}")
        top_track_uris = top_tracks.get_top_tracks(self.id)

        # print(f"Create tracks: {pendulum.now()}")
        all_tracks = {
            track.uri: track
            for track in track_features.create_tracks(
                list(saved_track_uris | playlist_track_uris | top_track_uris)
            )
        }

        # print(f"Suff: {pendulum.now()}")
        self.saved_tracks = {all_tracks[uri] for uri in saved_track_uris if uri in all_tracks}
        self.playlist_tracks = {all_tracks[uri] for uri in playlist_track_uris if uri in all_tracks}
        self.top_tracks = {all_tracks[uri] for uri in top_track_uris if uri in all_tracks}

        # print(f"Averaging: {pendulum.now()}")
        self.pref = average_features(all_tracks.values())

        # print(f"Combining: {pendulum.now()}")
        self.library = self.saved_tracks | self.playlist_tracks | self.top_tracks
        # print("{0}'s library updated. New size: {1}".format(self.spotipy.me()["display_name"], len(self.library)))
