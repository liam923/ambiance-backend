import threading
from dataclasses import dataclass
from time import sleep
from typing import Optional, List

import spotipy
from dataclasses_json import DataClassJsonMixin
import ambiance.model.db as db

REFRESH_RATE = 1.0
MODULAR_WALK_CYLCE = 7


def _update_user_queue(jukebox: "Jukebox", active):
    while jukebox.active:
        if not active:
            break

        if jukebox._last_queued is None:
            jukebox._add_to_queue()

        playback = jukebox._sp().current_playback()

        if playback is None:
            jukebox.active = False
        elif playback["item"]["uri"] == jukebox._last_queued:
            jukebox._add_to_queue()

        sleep(REFRESH_RATE)


@dataclass
class Jukebox(DataClassJsonMixin):
    id: str
    user_id: str
    session_id: str
    active: bool = False

    def __post_init__(self):
        self._i = 0
        self._last_queued: Optional[str] = None
        self._previously_queued_songs = set()

        self.update_jukebox_queue()

    def update_jukebox_queue(self):
        self._suggested_songs = [
            track.uri
            for track in db.DB().sessions[self.session_id].pool
        ]
        self._queue: List[str] = list(reversed(self._suggested_songs))

    def _resort_tracks(self, tracks: List[str]) -> List[str]:
        new_tracks = []
        for offset in range(0, MODULAR_WALK_CYLCE):
            step = 0
            i = offset
            while i < len(new_tracks):
                new_tracks.append(tracks[i])

                step += 1
                i = offset + (step * MODULAR_WALK_CYLCE)
        return new_tracks

    # instantiates the spotipy instance
    def _sp(self) -> spotipy.Spotify:
        return db.DB().users[self.user_id].spotipy

    # starts the function that checks whether the song is ending
    def start(self) -> bool:
        if self._sp().current_playback() is None:
            return False
        else:
            self.active = True
            self._thread = threading.Thread(target=_update_user_queue, args=(self, lambda : self.active))
            self._thread.start()

            return True

    def stop(self):
        if self._thread is not None:
            self.active = False

    def _add_to_queue(self) -> Optional[str]:
        next_song = self._next_song()
        if next_song is not None:
            self._last_queued = next_song
            db.DB().users[self.user_id].spotipy.add_to_queue(next_song)
            return next_song
        else:
            return None

    def _next_song(self) -> Optional[str]:
        if len(self._suggested_songs) == 0:
            return None

        while True:
            if len(self._queue) == 0:
                self._previously_queued_songs = set()
                self._queue = list(reversed(self._suggested_songs))
            else:
                next_song = self._queue.pop(-1)
                if next_song not in self._previously_queued_songs:
                    return next_song

    def __del__(self):
        try:
            if self._thread is not None:
                self.active = False
        except AttributeError:
            pass
