from dataclasses import dataclass
from typing import Optional

from dataclasses_json import DataClassJsonMixin


@dataclass
class LoginRequest(DataClassJsonMixin):
    redirect_uri: str
    state: Optional[str] = None


@dataclass
class AuthorizeRequest(DataClassJsonMixin):
    code: str
    state: Optional[str] = None
    error: Optional[str] = None


@dataclass
class State(DataClassJsonMixin):
    redirect_uri: str
    spotify_redirect_uri: str
    given_state: Optional[str] = None
