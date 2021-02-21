from typing import Set, List

import ambiance.model.db as db

from multiprocessing import Pool


def get_playlist_tracks(user_id: str) -> Set[str]:
    sp = db.DB().users[user_id].spotipy

    spotify_id = sp.me()['id']
    user_playlists = [playlist["uri"] for playlist in sp.user_playlists(spotify_id)["items"]]
    tracks = set()

    pool = Pool()

    all_tracks = pool.map(_playlist_to_tracks_pickled, ((uri, sp) for uri in user_playlists))
    tracks = {track for uris in all_tracks for track in uris}

    return tracks


def _playlist_to_tracks_pickled(params) -> Set[str]:
    playlist_uri, sp = params
    playlist_tracks = sp.playlist_items(playlist_uri)

    return {track["track"]["uri"] for track in playlist_tracks["items"]}


def playlist_to_tracks(user_id: str, playlist_uri: str) -> List[str]:
    sp = db.DB().users[user_id].spotipy
    tracks = set()
    playlist_tracks = sp.playlist_items(playlist_uri)
    playlist_tracks = playlist_tracks["items"]
    for track in playlist_tracks:
        track_uri = track["track"]["uri"]
        tracks.add(track_uri)
    return list(tracks)


def album_to_tracks(user_id:str, album_uri: str) -> List[str]:
    sp = db.DB().users[user_id].spotipy
    tracks = set()
    album_tracks = sp.album_tracks(album_id=album_uri)
    for track in album_tracks['items']:
        tracks.add(track["track"]["uri"])
    return list(tracks)




# get_playlist_tracks("spotify:playlist:3vsfAmGkWAVhcdcK6n033T?si=6DROcrIaRdSxIrrRq3yRxQ",
#                     "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOjE2MTM5NDQ1NDQsImlzcyI6ImFtYmlhbmNlLmJhY2tlbmQiLCJhdWQiOiJhbWJpYW5jZS5iYWNrZW5kIiwiaWF0IjoxNjEzODU4MTQ0LCJzdWIiOiI5YjRmZmQ1Zi03MWQ2LTRmODktOGFmNy1hZDk1NDE3ZjZkZWQifQ.DSpFW3nRnsaWj58FVUdWs8UPKTpQFvPEWnJjqwyVEDGILt3tS4stkNZwEBh3F9YYj0erdJl0cv7GEm4rJXwbaZ2YICDDReH8_ft38U6j0AP6qvIUWGc0dVAbVyOf6uRXlughbYFOBRzjYUIERqVcbp7WCxKJNZcudfZVEa9Blin59BAZ6pzZ6Wf5igzhu5hZhE10s0n0ZYM9RWmGLX_viOwQ-AkClCAvgE6QFLsnrJbAqzhAKBq2QpDAoZ0vsZw926VpNo2Ib6DkY1OHyd25tfNSt2C4rYXtqWkd479VKIiQYVeBy2Rm9LWjw3VcnXery32TU2IsrTwh_g1EUoR6iIkOUoQH-HZ29Y7EyG293U_8mRK6BgXoHp2G_yDafruPeth7LG8K7q8ZHtxJtNSxA7te-8dfiBg8ggOUXuV0RlxKVi_xTLy4UgF97wzh89BT79w1EPjBEjhVW2DF0P225hs_omEhdKQbj3KrmMsV51RvIhlvV55ZRnfqjHrWacKDpki0euq4ENmoRbG8vZDo6NCVC-wj4hNp_U-8FZNqseqY1dGjZexl909kyT52kud08ebrSoLHRZJlX7KQhJgzNvRzjpTX9B5gPw04uLERuaBaWxEUIpsjUZzZWGMvHrapHHttsSnX1GzFsBqRiY7qJNQSESmUcpIOvVjYPnO9qek")
