from multiprocessing import Pool
from typing import List, Collection, Set

import ambiance.model.db as db
from ambiance.feature_engine.features import vectorize_features
from ambiance.model.track import Track
import pendulum


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
    # eventually going to get this from user_id -> oAuth dict
    sp = db.CLIENT_SPOTIPY
    sp.trace = True

    tracks = list(chunks([track for track in tracks if track], 50))

    pool = Pool()

    feature_results = pool.map(_process_feature, ((sublist, sp) for sublist in tracks))
    # print(f"Track info time: {pendulum.now()}")
    track_info_results = pool.map(_process_track_info, ((sublist, sp) for sublist in tracks))

    res = set()

    for features, track_info in zip(feature_results, track_info_results):
        res |= {
            vectorize_features(features[key], track_info[key])
            for key in features
            if key in track_info
        }
    return res

    # return {
    #     vectorize_features(features[key], track_info[key])
    #     for key in features
    #     if key in track_info
    # }
    #
    #
    # features = []
    # track_info = []
    # for sublist in tracks:
    #     sublist = [track for track in sublist if ":local:" not in track]
    #     features.extend(track for track in sp.audio_features(sublist) if track)
    #     track_info.extend(track for track in sp.tracks(sublist)["tracks"] if track)
    #
    # features = sorted(features, key=lambda track: track["id"])
    # track_info = sorted(track_info, key=lambda track: track["id"])
    #
    # return {
    #     vectorize_features(track, info) for track, info in zip(features, track_info)
    # }


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


# demo
# print(get_tracks_features(['spotify:track:5TXDeTFVRVY7Cvt0Dw4vWW', 'spotify:track:2S2od3hT7ceytw7d1pTRuE']))
