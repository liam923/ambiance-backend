from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class Jukebox(DataClassJsonMixin):
    id: str
