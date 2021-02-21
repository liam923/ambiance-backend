from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

from dataclasses_json import DataClassJsonMixin

from ambiance.model.session import Session
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


if PERSISTENT_DB.exists():
    # DB = _DataBase.from_json(PERSISTENT_DB.read_text())
    DB = _DataBase()
else:
    DB = _DataBase()
