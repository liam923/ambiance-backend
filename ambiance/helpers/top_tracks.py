# Shows the top tracks for a user
from typing import Set
import ambiance.model.db as db


def get_top_tracks(user_id: str, limit: int = 100) -> Set[str]:
    response = []
    sp = db.DB().users[user_id].spotipy

    ranges = ['short_term', 'medium_term', 'long_term']

    for sp_range in ranges:
        results = sp.current_user_top_tracks(time_range=sp_range, limit=limit)
        for item in results['items']:
            response.append(item['uri'])
    return set(response)


# demo
# print(get_top_tracks(limit=2))
