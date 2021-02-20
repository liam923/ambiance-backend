import math

import numpy as np
from typing import Dict, List, Tuple, Any

from ambiance.model.track import Track


def vectorize_features(song: Dict[str, Any], track_info: Dict[str, Any]) -> Track:
    features = np.array(
            [
                song["danceability"],
                song["energy"],
                song["key"],
                song["loudness"],
                song["mode"],
                song["speechiness"],
                song["acousticness"],
                song["instrumentalness"],
                song["liveness"],
                song["valence"],
                song["tempo"],
            ]
        )

    return Track(song["uri"], track_info["name"], [artist["name"] for artist in track_info["artists"]], features)


def average_features(library: List[Track]) -> np.ndarray:
    feature_sum = np.zeros(11)

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
    library: List[Track], features: np.ndarray
) -> List[Track]:
    return sorted(library, key=lambda song: euclidean_distance(song.features, features))
