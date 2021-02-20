from dataclasses import field, dataclass
from typing import List
import uuid
from .helpers import top_tracks, track_features

from dataclasses_json import dataclass_json

from ambiance.endpoint.endpoint import endpoint, POST, PUT
from ..feature_engine.features import average_features
from ..model.db import DB
from ..model.user import User


@dataclass_json
@dataclass
class CreateInput:
    preferences: List[str] = field(default_factory=list)


@dataclass_json
@dataclass
class CreateOutput:
    session_id: str


@endpoint(method=POST, body=CreateInput)
def create(body: CreateInput, user: str, **kwargs) -> CreateOutput:
    new_id = uuid.uuid4()


@dataclass_json
@dataclass
class JoinInput:
    session_id: str


@endpoint(method=PUT, body=JoinInput)
def join(body: JoinInput, user: str, **kwargs) -> None:
    session = DB.sessions[body.session_id]
    if user not in session.users:
        session.users.append(user)

    DB.users[user].update()
