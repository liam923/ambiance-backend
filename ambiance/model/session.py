from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set

import numpy as np
from dataclasses_json import DataClassJsonMixin

from ambiance.endpoint.playlist import update
from ambiance.feature_engine.features import average_features, rank_library
from ambiance.helpers.playlist_tracks import playlist_to_tracks, album_to_tracks
from ambiance.helpers.track_features import create_tracks
from ambiance.model import db
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
    subscribed: Dict[str, str] = field(default_factory=dict)

    processed_data: SessionData = field(default_factory=SessionData)

    def vibe_check(self) -> None:
        if self.vibe is not None:
            if "playlist" in self.vibe:
                playlist_to_tracks(self.users[0], self.vibe)
            elif "album" in self.vibe:
                album_to_tracks(self.users[0], self.vibe)
            else:
                self.processed_data.vibe_feature_vector = create_tracks([self.vibe])[
                    0
                ].features
        else:
            vibe_pool = []
            for user in self.users:
                for track in db.DB().users[user].top_tracks:
                    if track not in vibe_pool:
                        vibe_pool.append(track)

            self.processed_data.vibe_feature_vector = average_features(vibe_pool)

    def update_pool(self) -> None:
        library: Set[Track] = set()
        for user in self.users:
            library |= db.DB().users[user].library

        self.vibe_check()
        self.pool = rank_library(library, self.processed_data.vibe_feature_vector)

        for jukebox in self.jukeboxes.values():
            jukebox.update_jukebox_queue()

        for user in self.subscribed:
            update(user, self.id)

    def change_vibe(self, uri: str = None) -> None:
        self.vibe = uri
        self.update_pool()
