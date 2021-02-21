from multiprocessing import Pool
from typing import Collection, Set

import ambiance.model.db as db
from ambiance.feature_engine.features import vectorize_features
from ambiance.model.track import Track


def _process_feature(params):
    sublist, sp = params
    sublist = [track for track in sublist if ":local:" not in track]

    features = {track["id"]: track for track in sp.audio_features(sublist) if track}

    return features


def _process_track_info(params):
    sublist, sp = params
    sublist = [track for track in sublist if ":local:" not in track]

    track_info = {track["id"]: track for track in sp.tracks(sublist)["tracks"] if track}

    return track_info


def create_tracks(tracks: Collection[str]) -> Set[Track]:
    sp = db.CLIENT_SPOTIPY
    sp.trace = True

    tracks = list(chunks([track for track in tracks if track], 50))

    pool = Pool()

    feature_results = pool.map(_process_feature, ((sublist, sp) for sublist in tracks))
    track_info_results = pool.map(_process_track_info, ((sublist, sp) for sublist in tracks))

    res = set()

    for features, track_info in zip(feature_results, track_info_results):
        res |= {
            vectorize_features(features[key], track_info[key])
            for key in features
            if key in track_info
        }
    return res


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
