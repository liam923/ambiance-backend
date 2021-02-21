from dataclasses import field, dataclass
from typing import List, Optional
import uuid

from dataclasses_json import dataclass_json

from ambiance.endpoint.endpoint import endpoint, POST, PUT
from ambiance.endpoint.endpoint import endpoint, POST
from ambiance.model.db import DB
from ambiance.model.session import Session


@dataclass_json
@dataclass
class CreateInput:
    vibe: Optional[str] = None


@dataclass_json
@dataclass
class CreateOutput:
    session_id: str


@endpoint(method=POST, body=CreateInput)
def create(body: CreateInput, user: str, **kwargs) -> CreateOutput:
    session_id = uuid.uuid4()

    # Update this user's preference
    master_user = DB.users[user]
    master_user.update_preference()
    master_user.update_library()

    session = Session(id=session_id, users=[user], pool=master_user.library)

    if body.vibes is None:
        session.change_vibe()
    else:
        session.change_vibe(body.vibe)

    DB.sessions.update(session_id, session)

    return CreateOutput(session_id=session_id)


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
    vibe: str


@endpoint(method=PUT, body=JoinInput)
def update(body: UpdateInput, **kwargs) -> None:
    DB.sessions[UpdateInput.session_id].change_vibe(UpdateInput.vibe)
