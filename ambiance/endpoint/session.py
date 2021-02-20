from dataclasses import field, dataclass
from typing import List

from dataclasses_json import dataclass_json

from ambiance.endpoint.endpoint import endpoint, POST


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
    pass
