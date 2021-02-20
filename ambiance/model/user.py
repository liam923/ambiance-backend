from dataclasses import dataclass, field

import spotipy
import numpy as np
from dataclasses_json import DataClassJsonMixin
from spotipy import Spotify
from typing import List

from ambiance.endpoint.helpers import top_tracks, track_features, saved_tracks
from ambiance.feature_engine.features import average_features
from ambiance.model.spotify_auth import Credentials
from ambiance.model.track import Track


@dataclass
class User(DataClassJsonMixin):
    id: str
    credentials: Credentials
    spotipy: Spotify = None
    library: List[Track] = field(default_factory=list)
    pref: np.ndarray = field(default_factory=lambda : np.array([]))

    def __post_init__(self):
        self.spotipy = spotipy.Spotify(client_credentials_manager=self.credentials)
        self.update()

    def update(self):
        self.update_preference()
        self.update_library()

    def update_preference(self) -> None:
        user_top_tracks = top_tracks.get_top_tracks(self.id)
        self.pref = average_features(track_features.create_tracks(user_top_tracks))

    def update_library(self) -> None:
        saved = saved_tracks.get_saved_tracks()
        self.library = track_features.create_tracks(saved)
