from typing import Tuple

from ambiance.model import db


def get_user(user_id: str) -> Tuple[str, str]:
    sp = db.DB().users[user_id].spotipy
    return sp.me()

