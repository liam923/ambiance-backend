from dataclasses import dataclass
from typing import Optional
import uuid

from dataclasses_json import DataClassJsonMixin

from ambiance.endpoint.endpoint import endpoint, POST, PUT
import ambiance.model.db as db
from ambiance.helpers import user_info
from ambiance.model.session import Session


@dataclass
class CreateInput(DataClassJsonMixin):
    vibe: Optional[str] = None
    live: bool = False


@dataclass
class CreateOutput(DataClassJsonMixin):
    session_id: str


@endpoint(method=POST, body=CreateInput)
def create(body: CreateInput, user: str, **kwargs) -> CreateOutput:
    session_id = str(uuid.uuid4())

    # Update this user's preference
    master_user = db.DB().users[user]
    master_user.update()

    username = user_info.get_user(user)['display_name']

    session = Session(id=session_id, users=[user], name=username + "'s Party")

    session.user_scale_map[user] = 0

    session.change_vibe(body.vibe)

    session.live = body.live

    db.DB().sessions[session_id] = session

    return CreateOutput(session_id=str(session_id))


@dataclass
class JoinInput(DataClassJsonMixin):
    session_id: str


@dataclass
class JoinOutput(DataClassJsonMixin):
    session_id: str


@endpoint(method=PUT, body=JoinInput)
def join(body: JoinInput, user: str, **kwargs) -> JoinOutput:
    session = db.DB().sessions[body.session_id]
    if user not in session.users:
        session.users.append(user)
        session.update_pool()
        session.user_scale_map[user] = 0

    db.DB().users[user].update()
    return JoinOutput(body.session_id)


@dataclass
class UpdateInput(DataClassJsonMixin):
    session_id: str
    vibe: Optional[str] = None
    live_playlist: Optional[bool] = None


@dataclass
class UpdateOutput(DataClassJsonMixin):
    session_id: str


@endpoint(method=PUT, body=UpdateInput)
def update(body: UpdateInput, **kwargs) -> UpdateOutput:
    sesh = db.DB().sessions[body.session_id]
    if body.vibe is not None:
        sesh.change_vibe(body.vibe)
    if body.live_playlist is not None:
        sesh.live = body.live_playlist
    return UpdateOutput(body.session_id)
