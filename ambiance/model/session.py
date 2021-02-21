from dataclasses import dataclass, field
from typing import List, Dict, Optional

import numpy as np
from dataclasses_json import DataClassJsonMixin

from ambiance.endpoint.playlist import update
from ambiance.feature_engine.features import average_features, rank_library
from ambiance.helpers import top_tracks, saved_tracks, playlist_tracks
from ambiance.helpers.track_features import create_tracks
from ambiance.model.jukebox import Jukebox
from ambiance.model.track import Track


@dataclass
class SessionData(DataClassJsonMixin):
    vibe_feature_vector: np.ndarray = field(default_factory=lambda: np.ndarray([]))


@dataclass
class Session(DataClassJsonMixin):
    id: str
    users: List[str] = field(default_factory=list)
    name: str = ""
    jukeboxes: Dict[str, Jukebox] = field(default_factory=dict)
    vibe: Optional[str] = None
    pool: List[Track] = field(default_factory=list)
    live: bool = True
    subscribed: Dict[str, str] = field(default_factory=dict)

    processed_data: SessionData = field(default_factory=SessionData)

    def vibe_check(self) -> None:
        if self.vibe is not None:
            if "playlist" in self.vibe:
                pass
            else:
                self.processed_data.vibe_feature_vector = create_tracks([self.vibe])[0].features
        else:
            vibe_pool = []
            for user in self.users:
                user_top_tracks = top_tracks.get_top_tracks(user)
                for track in user_top_tracks:
                    if track not in vibe_pool:
                        vibe_pool.append(track)

            self.processed_data.vibe_feature_vector = average_features(create_tracks(vibe_pool))

    def update_pool(self) -> None:
        new_pool = set()

        for user in self.users:
            user_tracks = set()
            user_tracks.update(saved_tracks.get_saved_tracks(user))
            user_tracks.update(playlist_tracks.get_playlist_tracks(user))
            user_tracks.update(top_tracks.get_top_tracks(user))
            for track in create_tracks(list(user_tracks)):
                new_pool.add(track)

        self.vibe_check()
        self.pool = rank_library(list(new_pool), self.processed_data.vibe_feature_vector)

        if self.live:
            for user in self.subscribed:
                update(user, self.id)


    def change_vibe(self, uri: str = None) -> None:
        self.vibe = uri
        self.update_pool()
