# Shows a user's saved tracks (need to be authenticated via oauth)
from multiprocessing import Pool
from typing import Set

import ambiance.model.db as db

scope = "user-library-read"


LIMIT = 50


def _process(params) -> Set[str]:
    offset, sp = params
    results = sp.current_user_saved_tracks(limit=LIMIT, offset=offset * LIMIT)
    return {item["track"]["uri"] for item in results["items"]}


def get_saved_tracks(user_id: str) -> Set[str]:
    response = set()
    sp = db.DB().users[user_id].spotipy

    results = sp.current_user_saved_tracks(limit=LIMIT)
    for item in results["items"]:
        response.add(item["track"]["uri"])

    total = results["total"]

    pool = Pool()
    map_res = pool.map(_process, ((x, sp) for x in range(1, total // LIMIT + 1)))
    return {uri for uris in map_res for uri in uris} | response

