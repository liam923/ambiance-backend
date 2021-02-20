from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
from dataclasses_json import DataClassJsonMixin

from ambiance.model.jukebox import Jukebox
from ambiance.model.user import User


@dataclass
class SessionData(DataClassJsonMixin):
    vibe_feature_vector: np.ndarray


@dataclass
class Session(DataClassJsonMixin):
    id: str
    users: Dict[str, User]
    jukeboxes: Dict[str, Jukebox]
    preferences: Optional[str]

    processed_data: SessionData
