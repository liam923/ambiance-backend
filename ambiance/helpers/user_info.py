from typing import Tuple

from django.http import JsonResponse

from ambiance.model import db


def get_user(user_id: str) -> Tuple[str, str]:
    sp = db.DB.users[user_id].spotipy
    return sp.me()


print(get_user(""))
