import json
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from typing import Dict, Optional

import spotipy
from dataclasses_json import DataClassJsonMixin

from ambiance.keys import spotify
from ambiance.model.session import Session
from ambiance.model.spotify_auth import Credentials
from ambiance.model.user import User

PERSISTENT_DB = Path(__file__).parent.parent / "keys" / "secret" / "bd.json"


@dataclass
class _DataBase(DataClassJsonMixin):
    sessions: Dict[str, Session] = field(default_factory=dict)
    users: Dict[str, User] = field(default_factory=dict)

    def save(self):
        for user in self.users.values():
            user.spotipy = None
        PERSISTENT_DB.write_text(self.to_json())


# if PERSISTENT_DB.exists():
#     d = json.loads(PERSISTENT_DB.read_text())
#
#     _db = _DataBase()
#     _db.users = {u["id"]: User(id=u["id"], credentials=Credentials.from_dict(u["credentials"])) for u in
#                  d["users"].values()}
# else:
#     _db = _DataBase()


CLIENT_CREDENTIALS = spotipy.SpotifyClientCredentials(
    client_id=spotify.CLIENT_ID, client_secret=spotify.CLIENT_SECRET
)
CLIENT_SPOTIPY = spotipy.Spotify(oauth_manager=CLIENT_CREDENTIALS)


_db = None


def DB() -> _DataBase:
    global _db
    if _db is None:

        if PERSISTENT_DB.exists():
            d = json.loads(PERSISTENT_DB.read_text())

            _db = _DataBase()
            for u in d["users"].values():
                user = User.__new__(User)
                user.id = u["id"]
                user.credentials = Credentials.from_dict(u["credentials"])
                user.spotipy = spotipy.Spotify(
                    client_credentials_manager=user.credentials
                )
                _db.users[u["id"]] = user

            # _db.users = {u["id"]: User(id=u["id"], credentials=Credentials.from_dict(u["credentials"])) for u in d["users"].values()}
        else:
            _db = _DataBase()
    return _db
