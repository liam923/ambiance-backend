from pathlib import Path
from warnings import warn

public_key_file: Path = Path(__file__).parent / "secret" / "jwt.key.pub"
private_key_file: Path = Path(__file__).parent / "secret" / "jwt.key"

if public_key_file.exists():
    PUBLIC = public_key_file.read_text()
else:
    warn(f"Could not find public key file at {private_key_file.absolute()}")
    PUBLIC = ""

if private_key_file.exists():
    PRIVATE = private_key_file.read_text()
else:
    warn(f"Could not find private key file at {private_key_file.absolute()}")
    PRIVATE = ""
