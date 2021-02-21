import uuid
from dataclasses import dataclass
from typing import Optional

from dataclasses_json import DataClassJsonMixin

from ambiance.endpoint.endpoint import *
import ambiance.model.db as db
from ambiance.model.jukebox import Jukebox


@dataclass
class StartJukeboxRequest(DataClassJsonMixin):
    session_id: str
    jukebox_id: Optional[str] = None


@dataclass
class StartJukeboxResponse(DataClassJsonMixin):
    jukebox_id: str
    jukebox_exists: bool


@endpoint(method=POST, body=StartJukeboxRequest)
def start(body: StartJukeboxRequest, user: str, **kwargs) -> StartJukeboxResponse:
    if body.jukebox_id is not None:
        jukebox_id = body.jukebox_id
        jukebox = db.DB().sessions[body.session_id].jukeboxes[body.jukebox_id]
    else:
        jukebox_id = str(uuid.uuid4())
        jukebox = Jukebox(id=jukebox_id, user_id=user, session_id=body.session_id)

    for jukebox in db.DB().sessions[body.session_id].jukeboxes.values():
        if jukebox.user_id == user and jukebox.active:
            raise(Error(409))

    db.DB().sessions[body.session_id].jukeboxes[jukebox_id] = jukebox
    if not jukebox.start():
        raise Error(406)

    return StartJukeboxResponse(jukebox_id, jukebox_exists=False)


@dataclass
class StopJukeboxRequest(DataClassJsonMixin):
    session_id: str
    jukebox_id: str


@dataclass
class StopJukeboxResponse(DataClassJsonMixin):
    success: bool


@endpoint(method=POST, body=StopJukeboxRequest)
def stop(body: StopJukeboxRequest, user: str, **kwargs) -> StopJukeboxResponse:
    jukebox = db.DB().sessions[body.session_id].jukeboxes[body.jukebox_id]
    jukebox.stop()

    return StopJukeboxResponse(True)
