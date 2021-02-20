import numpy as np
from typing import Dict, List

def vectorize_features(song: Dict[str, float]) -> tuple[str, ndarray]:
  return {song["id"]: np.array([song["danceability"],
    song["energy"],
    song["key"],
    song["loudness"],
    song["mode"],
    song["speechiness"],
    song["acousticness"],
    song["instrumentalness"],
    song["liveness"],
    song["valence"],
    song["tempo"]
  ])}


def average_features(library: List[tuple[str, ndarray]]) -> ndarray:
  feature_sum = np.zeroes(11)

  feature_count = 0.

  for song in library:
  feature_sum += library[song]
  feature_count += 1

  return feature_sum / feature_count


def euclidean_distance(first: ndarray, second: ndarray, scale: float=1.) -> float:

  dist = np.copy(first)
  dist -= second
  dist = np.power(dist, 2.)
  
  return (numpy.sum(dist) ^ 0.5) * scale

def rank_library(library: List[tuple[str, ndarray]], features: ndarray) -> List[tuple[str, ndarray]]:
  return sorted(library, key=lambda song: euclidean_distance(song[1], features))