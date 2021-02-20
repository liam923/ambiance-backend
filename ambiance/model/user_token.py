from dataclasses import dataclass

from dataclasses_json import dataclass_json
from pendulum import DateTime


@dataclass_json
@dataclass
class UserToken:
    exp: DateTime
    iss: str
    aud: str
    iat: DateTime
    sub: str
