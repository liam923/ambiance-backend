from dataclasses import dataclass
from pathlib import Path

from dataclasses_json import dataclass_json

secret_file: Path = Path(__file__).parent / "secret" / "spotify.json"


@dataclass_json
@dataclass
class _SpotifySecrets:
    CLIENT_ID: str
    CLIENT_SECRET: str


if secret_file.exists():
    secrets = _SpotifySecrets.from_json(secret_file.read_text())
else:
    secrets = _SpotifySecrets(CLIENT_ID="", CLIENT_SECRET="")

CLIENT_ID = secrets.CLIENT_ID
CLIENT_SECRET = secrets.CLIENT_SECRET
