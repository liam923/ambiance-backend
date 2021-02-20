from dataclasses import field, dataclass
from typing import List
import uuid

from dataclasses_json import dataclass_json

from ambiance.endpoint.endpoint import endpoint, POST, PUT
from ambiance.endpoint.endpoint import endpoint, POST
from ambiance.model.db import DB
from ambiance.model.session import Session


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
    session_id = uuid.uuid4()

    # Update this user's preference
    DB.users[user].update_preference()

    session = Session(id=session_id, users=[user])

    DB.sessions.update(session_id, session)


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


@dataclass_json
@dataclass
class UpdateInput:
    session_id: str
    vibe: any


@endpoint(method=PUT, body=JoinInput)
def update(body: UpdateInput, **kwargs) -> None:
    pass
