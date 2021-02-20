from dataclasses import dataclass, field
from typing import Dict

from dataclasses_json import DataClassJsonMixin


@dataclass
class _DataBase(DataClassJsonMixin):
    sessions: Dict[str, Session] = field(default_factory=dict)
    users: Dict[str, User] = field(default_factory=dict)


DB = _DataBase()
