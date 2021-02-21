from dataclasses import dataclass
from threading import Timer
from typing import Optional

import spotipy
from dataclasses_json import DataClassJsonMixin
import ambiance.model.db as db


REFRESH_RATE = 5.0


@dataclass
class Jukebox(DataClassJsonMixin):
    id: str
    user_id: str
    active: bool = False

    def __post_init__(self):
        self._timer: Optional[Timer] = None
        self._i = 0

    # instantiates the spotipy instance
    def _sp(self) -> spotipy.Spotify:
        return db.DB().users[self.user_id].spotipy

    # starts the function that checks whether the song is ending
    def start(self):
        timer = Timer(0.0, lambda: self._update_queue())
        timer.start()
        self._timer = timer

    #  Adds to the queue if there is less than 5 seconds left in the song – every REFRESH_RATE seconds recurs
    def _update_queue(self):
        self._timer = Timer(REFRESH_RATE, lambda: self._update_queue())
        self._timer.start()

        playback = self._sp().current_playback()
        time_left = playback["item"]["duration_ms"] - playback["progress_ms"] if playback else 0

        if time_left <= REFRESH_RATE * 1000:
            self._add_to_queue()

    def stop(self):
        if self._timer is not None:
            self._timer.cancel()

    def _add_to_queue(self) -> str:
        new_song = self._next_song()
        db.DB().users[self.user_id].spotipy.add_to_queue(new_song)
        return new_song

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
