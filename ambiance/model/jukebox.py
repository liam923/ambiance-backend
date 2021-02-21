import threading
from dataclasses import dataclass
from threading import Timer
from time import sleep
from typing import Optional

import spotipy
from dataclasses_json import DataClassJsonMixin
import ambiance.model.db as db


REFRESH_RATE = 1.0


def _update_queue(jukebox: "Jukebox"):
    while jukebox.active:
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
    active: bool = False

    def __post_init__(self):
        self._timer: Optional[Timer] = None
        self._i = 0
        self._last_queued: Optional[str] = None

    # instantiates the spotipy instance
    def _sp(self) -> spotipy.Spotify:
        return db.DB().users[self.user_id].spotipy

    # starts the function that checks whether the song is ending
    def start(self) -> bool:
        print(self._sp().current_playback())
        if self._sp().current_playback() is None:
            return False
        else:
            self.active = True
            self._thread = threading.Thread(target=_update_queue, args=(self,))
            self._thread.start()

            return True

    def stop(self):
        if self._timer is not None:
            self.active = False

    def _add_to_queue(self) -> str:
        self._last_queued = self._next_song()

        db.DB().users[self.user_id].spotipy.add_to_queue(self._last_queued)
        return self._last_queued

    def _next_song(self) -> str:
        songs = [
            "spotify:track:0S78qezX3QdsGDp3LPhV7T",
            "spotify:track:21xkL3U23GZEhp4uM1NSaM",
            "spotify:track:3YYQzADAn5QHbVZaFEOPYq",
            "spotify:track:1NiYMmNWaIQTODcA06EYDa",
            "spotify:track:6XQ5aL7MBe19t9cvFMKiEo",
            "spotify:track:4GU1f49npUvGSn4dEB0UOi",
            "spotify:track:5QXDD5E0bWRdsgW0bQTYRG",
            "spotify:track:3mKg5P4GPGAc1tNKA3H3zI",
            "spotify:track:2gbqwypcMlSQLJosaYvvll",
            "spotify:track:54zMkQWwYLKTAx2qIkl45X",
            "spotify:track:3mk0bCojn7e3DuLuSQ0fHH",
            "spotify:track:1nEBO2jgdDBT9LxNyoiOPw",
            "spotify:track:3q6bWbi0APjVopR2oxv2jV",
            "spotify:track:7AUnx49FMBFBQTQdmBpJJE",
            "spotify:track:7IzyGb9fXAAJTQrahYNaIA",
            "spotify:track:27kbv0zhEhp3cgzcCMHq8r",
            "spotify:track:1qm1QdZKGvuRnNPDv04OmU",
        ]

        self._i += 1
        return songs[(self._i - 1) % len(songs)]

    def __del__(self):
        try:
            if self._timer is not None:
                self._timer.cancel()
        except AttributeError:
            pass
