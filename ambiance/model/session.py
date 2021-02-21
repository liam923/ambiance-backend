from dataclasses import dataclass
from typing import List, Dict, Optional

import numpy as np
from dataclasses_json import DataClassJsonMixin

from ambiance.feature_engine.features import average_features, rank_library
from ambiance.helpers import top_tracks, saved_tracks
from ambiance.helpers.track_features import create_tracks
from ambiance.model.jukebox import Jukebox
from ambiance.model.track import Track


@dataclass
class SessionData(DataClassJsonMixin):
    vibe_feature_vector: np.ndarray


@dataclass
class Session(DataClassJsonMixin):
    id: str
    users: List[str]
    name: str
    jukeboxes: Dict[str, Jukebox]
    vibe: Optional[str]
    pool: List[Track]

    processed_data: SessionData

    def vibe_check(self) -> np.ndarray:
        if self.vibe is not None:
            if "playlist" in self.vibe:
                pass
            else:
                return create_tracks([self.vibe])[0].features
        else:
            vibe_pool = []
            for user in self.users:
                user_top_tracks = top_tracks.get_top_tracks(user)
                for track in user_top_tracks:
                    if track not in vibe_pool:
                        vibe_pool.append(track)

            return average_features(vibe_pool)

    def update_pool(self) -> None:
        new_pool = []

        for user in self.users:
            user_saved_songs = create_tracks(saved_tracks.get_saved_tracks(user))
            for track in user_saved_songs:
                if track not in new_pool:
                    new_pool.append(track)

        self.pool = rank_library(self.vibe_check())

    def change_vibe(self, uri: str = None) -> None:
        self.vibe = uri
        self.update_pool()
