from dataclasses import field, dataclass
from typing import List
import uuid

from dataclasses_json import dataclass_json

from ambiance.endpoint.endpoint import endpoint, POST
from ambiance.model.db import DB


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

    res = str(DB.users[user].spotipy.artist_albums("spotify:artist:2WX2uTcsvV5OnS0inACecP", album_type='album'))

    return CreateOutput(res)
