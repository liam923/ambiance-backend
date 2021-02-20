import uuid
from json import JSONDecodeError
from typing import Optional

import jwt
from pendulum import DateTime

from ambiance.keys import jwt as key
from ambiance.model.user_token import UserToken


ALGORITHM = "RS256"
SERVER_NAME = "ambiance.backend"


def issue(user: Optional[str] = None) -> str:
    if user is None:
        user = str(uuid.uuid4())

    token = UserToken(
        exp=DateTime.now().add(days=1),
        sub=user,
        iat=DateTime.now(),
        iss=SERVER_NAME,
        aud=SERVER_NAME,
    )

    return jwt.encode(token.to_dict(), key.PRIVATE, algorithm=ALGORITHM)


def verify(token: str) -> Optional[str]:
    try:
        token_dict = jwt.decode(token, key.PUBLIC, algorithms=ALGORITHM, audience=SERVER_NAME)
        decoded = UserToken.from_dict(token_dict)
    except Exception:
        return None

    return decoded.sub
