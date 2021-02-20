# Shows a user's saved tracks (need to be authenticated via oauth)
from typing import List

import spotipy

from credentials import credentials

scope = 'user-library-read'


def get_saved_tracks() -> List[str]:
    response = []
    sp = spotipy.Spotify(client_credentials_manager=credentials)

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
