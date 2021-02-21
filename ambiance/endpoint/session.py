from dataclasses import dataclass
from typing import Optional
import uuid

from dataclasses_json import DataClassJsonMixin

from ambiance.endpoint.endpoint import endpoint, POST, PUT
import ambiance.model.db as db
from ambiance.model.session import Session


@dataclass
class CreateInput(DataClassJsonMixin):
    vibe: Optional[str] = None


@dataclass
class CreateOutput(DataClassJsonMixin):
    session_id: str


@endpoint(method=POST, body=CreateInput)
def create(body: CreateInput, user: str, **kwargs) -> CreateOutput:
    session_id = str(uuid.uuid4())

    # Update this user's preference
    master_user = db.DB().users[user]
    master_user.update_preference()
    master_user.update_library()

    session = Session(id=session_id, users=[user])

    session.change_vibe(body.vibe)

    DB.sessions.update(session_id, session)

    return CreateOutput(session_id=str(session_id))


@dataclass
class JoinInput(DataClassJsonMixin):
    session_id: str


@endpoint(method=PUT, body=JoinInput)
def join(body: JoinInput, user: str, **kwargs) -> None:
    session = DB().sessions[body.session_id]
    if user not in session.users:
        session.users.append(user)
        session.update_pool()

    db.DB().users[user].update()


@dataclass
class UpdateInput(DataClassJsonMixin):
    session_id: str
    vibe: str


@endpoint(method=PUT, body=JoinInput)
def update(body: UpdateInput, **kwargs) -> None:
    db.DB().sessions[body.session_id].change_vibe(body.vibe)
