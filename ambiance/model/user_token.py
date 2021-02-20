from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin
from pendulum import DateTime


@dataclass
class UserToken(DataClassJsonMixin):
    exp: DateTime
    iss: str
    aud: str
    iat: DateTime
    sub: str
