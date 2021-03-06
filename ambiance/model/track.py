from dataclasses import dataclass
from typing import List

import numpy as np
from dataclasses_json import DataClassJsonMixin


@dataclass
class Track(DataClassJsonMixin):
    uri: str
    name: str
    artists: List[str]
    features: np.ndarray

    def __eq__(self, other):
        return self.uri == other.uri

    def __hash__(self):
        return str.__hash__(self.uri)
