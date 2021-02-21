from django.http import JsonResponse

from ambiance.model import db


def search(query: str, user_id: str) -> JsonResponse:
    sp = db.DB().users[user_id].spotipy
    response = sp.search(query)
    return response
