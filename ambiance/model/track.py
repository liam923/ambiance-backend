from dataclasses import dataclass

import numpy as np
from dataclasses_json import DataClassJsonMixin


@dataclass
class Track(DataClassJsonMixin):
    uri: str
    name: str
    artists: List[str]
    features: np.ndarray

