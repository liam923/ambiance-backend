from dataclasses import dataclass

import spotipy
from dataclasses_json import DataClassJsonMixin
from spotipy import Spotify

from ambiance.model.spotify_auth import Credentials


@dataclass
class User(DataClassJsonMixin):
    id: str
    credentials: Credentials
    spotipy: Spotify = None

    def __post_init__(self):
        self.spotipy = spotipy.Spotify(client_credentials_manager=self.credentials)
