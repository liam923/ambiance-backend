# Shows the top tracks for a user
from typing import List

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_top_tracks(userId: str = "", limit: int = 50) -> List[str]:
    response = []
    scope = 'user-top-read'

    # eventually going to get this from user_id -> oAuth dict
    sp = spotipy.Spotify(
        oauth_manager=SpotifyOAuth(scope=scope))

    ranges = ['short_term', 'medium_term', 'long_term']

    print("range:", 'short_term')
    results = sp.current_user_top_tracks(time_range='short_term', limit=limit)
    for item in results['items']:
        response.append(item['uri'])
    return response


# demo
print(get_top_tracks(limit=2))
