# Shows a user's saved tracks (need to be authenticated via oauth)
from typing import Set

import spotipy

import ambiance.model.db as db

scope = 'user-library-read'


def get_saved_tracks(user_id: str) -> Set[str]:
    response = set()
    sp = db.DB().users[user_id].spotipy

    results = sp.current_user_saved_tracks()
    for item in results['items']:
        response.add(item['track']['uri'])

    while results['next']:
        results = sp.next(results)
        for item in results['items']:
            response.add(item['track']['uri'])

    return response


# demo
# print(get_saved_tracks())
