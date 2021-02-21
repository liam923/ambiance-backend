from datetime import date
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ambiance.model.db import DB
from ambiance.endpoint.endpoint import endpoint, POST

PLAYLIST_LENGTH: int = 100  # Cannot be over 100, it will break if you set as more than 100, don't be a dick


@dataclass_json
@dataclass
class CreatePlaylistInput:
    session_id: str
    playlist_id: str = ""
    playlist_name: str = ""


@dataclass_json
@dataclass
class CreatePlaylistOutput:
    session_id: str


# Generates the playlist for a user or regenerates the playlist
@endpoint(method=POST, body=CreatePlaylistInput)
def create(body: CreatePlaylistInput, user: str, **kwargs) -> CreatePlaylistOutput:
    # instantiates spotipy
    sp = DB().users[user].spotipy
    # creates list of song uris
    uri_list = [track.uri for track in DB().sessions[body.session_id].pool]
    # if there is no playlist name passed
    if body.playlist_name == "":
        # name the playlist after the session
        body.playlist_name = DB().sessions[body.session_id].name
    # creates the playlist with the new name
    spotify_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=spotify_id, name=body.playlist_name,
                                       description="Playlist generated by Ambiance on " +
                                                   date.today().strftime("%B %d, %Y"))
    # adds the tracks
    sp.playlist_add_items(playlist["id"], uri_list[:PLAYLIST_LENGTH])

    return CreatePlaylistOutput(body.session_id)


# updates the playlist with new tracks
def update(user_id: str, session_id: str, playlist_id: str):
    # instantiates spotipy
    sp = DB().users[user_id].spotipy
    # creates list of song uris
    uri_list = [track.uri for track in DB().sessions[session_id].pool]
    # replace all the tracks with the new pool of tracks
    sp.user_playlist_replace_tracks(user_id, playlist_id, *uri_list)
