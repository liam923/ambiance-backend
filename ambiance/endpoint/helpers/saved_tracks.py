# Shows a user's saved tracks (need to be authenticated via oauth)
from typing import List

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = 'user-library-read'


def get_saved_tracks() -> List[str]:
    response = []
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.current_user_saved_tracks()
    for item in results['items']:
        response.append(item['track']['uri'])

    while results['next']:
        results = sp.next(results)
        for item in results['items']:
            response.append(item['track']['uri'])

    return response


# demo
print(get_saved_tracks())
