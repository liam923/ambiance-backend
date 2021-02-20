from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin
from spotipy import Spotify

from ambiance.model.spotify_auth import Credentials


@dataclass
class User(DataClassJsonMixin):
    id: str
    credentials: Credentials
    spotipy: Spotify
