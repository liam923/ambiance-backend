from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, DefaultDict

import numpy as np
from dataclasses_json import DataClassJsonMixin

from ambiance.endpoint.playlist import update
from ambiance.feature_engine.features import average_features, rank_library
import ambiance.helpers.playlist_tracks as playlist_tracks
import ambiance.helpers.track_features as track_features
import ambiance.model.db as db
from ambiance.model.jukebox import Jukebox
from ambiance.model.track import Track

LIB_SIZE_SCALE_FACTOR = 0.5

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
    user_scale_map: DefaultDict[str, float] = field(default_factory=defaultdict)

    processed_data: SessionData = field(default_factory=SessionData)

    def vibe_check(self) -> None:
        if self.vibe is not None:
            if "playlist" in self.vibe:
                playlist_tracks.playlist_to_tracks(self.users[0], self.vibe)
            elif "album" in self.vibe:
                playlist_tracks.album_to_tracks(self.users[0], self.vibe)
            else:
                self.processed_data.vibe_feature_vector = list(track_features.create_tracks([self.vibe]))[
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
        users = db.DB().users
        user_size = {}
        for user in self.users:
            user_size[user] = len(users[user].library)

        max_library_size = user_size[max(user_size, key=lambda x: user_size[x])]
        # print("Max library size: {0}".format(max_library_size))
        user_scale_map = {user: ((size + max_library_size * LIB_SIZE_SCALE_FACTOR)
                                 / (max_library_size + max_library_size * LIB_SIZE_SCALE_FACTOR))
                          for (user, size) in user_size.items()}

        for user in user_scale_map:
            if user_scale_map[user] > 1.0:
                user_scale_map[user] = 1.0
            # print("{0}: {1}".format(users[user].spotipy.me()["display_name"], user_scale_map[user]))

        scale_map = {}
        for user in self.users:
            init_len = len(library)
            library |= users[user].library
            # print("Library: {0} -> {1}".format(init_len, len(library)))

            user_scale = user_scale_map[user]
            for track in users[user].library:
                if track.uri in scale_map:
                    scale_map[track.uri] = user_scale if user_scale < scale_map[track.uri] else scale_map[track.uri]
                else:
                    scale_map[track.uri] = user_scale

        self.vibe_check()
        self.pool = rank_library(library, self.processed_data.vibe_feature_vector, scale_map=scale_map)

        for jukebox in self.jukeboxes.values():
            jukebox.update_jukebox_queue()

        for user in self.subscribed:
            update(user, self.id)

    def change_vibe(self, uri: str = None) -> None:
        self.vibe = uri
        self.update_pool()
