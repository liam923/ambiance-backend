from typing import Set, List

import ambiance.model.db as db

from multiprocessing import Pool


def get_playlist_tracks(user_id: str) -> Set[str]:
    sp = db.DB().users[user_id].spotipy

    spotify_id = sp.me()['id']
    user_playlists = [playlist["uri"] for playlist in sp.user_playlists(spotify_id)["items"]]

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
        tracks.add(track["uri"])
    return list(tracks)
