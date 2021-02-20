# Shows a user's saved tracks (need to be authenticated via oauth)
from typing import List

import spotipy

from ambiance.model.db import DB

scope = 'user-library-read'


def get_saved_tracks(user_id: str) -> List[str]:
    response = []
    sp = DB.users[user_id].spotipy

    results = sp.current_user_saved_tracks()
    for item in results['items']:
        response.append(item['track']['uri'])

    while results['next']:
        results = sp.next(results)
        for item in results['items']:
            response.append(item['track']['uri'])

    return response


# demo
# print(get_saved_tracks())
