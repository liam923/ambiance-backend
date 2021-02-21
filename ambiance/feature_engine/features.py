import math

import numpy as np
from typing import Dict, List, Tuple, Any, Iterable

from ambiance.model.track import Track


def vectorize_features(song: Dict[str, Any], track_info: Dict[str, Any]) -> Track:
    raw = [
        song["danceability"],
        song["energy"],
        -song["loudness"],
        song["acousticness"],
        song["valence"],
        song["tempo"],
    ]
    raw_max = max(raw)
    raw_min = min(raw)

    features = np.array(
            [((x - raw_min) / (raw_max - raw_min)) for x in raw]
        )

    return Track(song["uri"], track_info["name"], [artist["name"] for artist in track_info["artists"]], features)


def average_features(library: Iterable[Track]) -> np.ndarray:
    feature_sum = np.zeros(6)

    feature_count = 0.0

    for song in library:
        feature_sum += song.features
        feature_count += 1

    return feature_sum / feature_count


def euclidean_distance(
    first: np.ndarray, second: np.ndarray, scale: float = 1.0
) -> float:

    dist = np.copy(first)
    dist -= second
    dist = np.power(dist, 2.0)
    return math.pow(np.sum(dist).tolist(), 0.5) * scale


def rank_library(
    library: Iterable[Track], features: np.ndarray, scale_map: Dict[str, float]
) -> List[Track]:
    return sorted(library, key=lambda song: euclidean_distance(song.features, features, scale=scale_map[song.uri]))
