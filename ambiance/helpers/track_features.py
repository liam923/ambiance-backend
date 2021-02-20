from typing import List, Dict, Tuple

import numpy as np

from ambiance.feature_engine.features import vectorize_features
from ambiance.model.db import DB


def get_tracks_features(tracks: List[str]) -> List[Tuple[str, np.ndarray]]:
    sp = DB.users[
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOjE2MTM5NDQ1NDQsImlzcyI6ImFtYmlhbmNlLmJhY2tlbmQiLCJhdWQiOiJhbWJpYW5jZS5iYWNrZW5kIiwiaWF0IjoxNjEzODU4MTQ0LCJzdWIiOiI5YjRmZmQ1Zi03MWQ2LTRmODktOGFmNy1hZDk1NDE3ZjZkZWQifQ.DSpFW3nRnsaWj58FVUdWs8UPKTpQFvPEWnJjqwyVEDGILt3tS4stkNZwEBh3F9YYj0erdJl0cv7GEm4rJXwbaZ2YICDDReH8_ft38U6j0AP6qvIUWGc0dVAbVyOf6uRXlughbYFOBRzjYUIERqVcbp7WCxKJNZcudfZVEa9Blin59BAZ6pzZ6Wf5igzhu5hZhE10s0n0ZYM9RWmGLX_viOwQ-AkClCAvgE6QFLsnrJbAqzhAKBq2QpDAoZ0vsZw926VpNo2Ib6DkY1OHyd25tfNSt2C4rYXtqWkd479VKIiQYVeBy2Rm9LWjw3VcnXery32TU2IsrTwh_g1EUoR6iIkOUoQH-HZ29Y7EyG293U_8mRK6BgXoHp2G_yDafruPeth7LG8K7q8ZHtxJtNSxA7te-8dfiBg8ggOUXuV0RlxKVi_xTLy4UgF97wzh89BT79w1EPjBEjhVW2DF0P225hs_omEhdKQbj3KrmMsV51RvIhlvV55ZRnfqjHrWacKDpki0euq4ENmoRbG8vZDo6NCVC-wj4hNp_U-8FZNqseqY1dGjZexl909kyT52kud08ebrSoLHRZJlX7KQhJgzNvRzjpTX9B5gPw04uLERuaBaWxEUIpsjUZzZWGMvHrapHHttsSnX1GzFsBqRiY7qJNQSESmUcpIOvVjYPnO9qek"].spotipy
    sp.trace = True

    features = sp.audio_features(tracks)

    feature_map = [vectorize_features(track) for track in features]

    return feature_map

# demo
# print(get_tracks_features(['spotify:track:5TXDeTFVRVY7Cvt0Dw4vWW', 'spotify:track:2S2od3hT7ceytw7d1pTRuE']))
