from dataclasses import dataclass
from typing import Optional

import pendulum
import requests
from dataclasses_json import DataClassJsonMixin
from pendulum import DateTime

from ambiance.keys import spotify


@dataclass
class Credentials(DataClassJsonMixin):
    refresh_token: str
    access_token: Optional[str] = None
    access_token_expiration: Optional[DateTime] = None

    @staticmethod
    def from_response(response: dict) -> "Credentials":
        return Credentials(
            refresh_token=response["refresh_token"],
            access_token=response["access_token"],
            access_token_expiration=pendulum.now().add(seconds=response["expires_in"]),
        )

    def get_access_token(self):
        if not self.access_token or self.access_token_expiration < pendulum.now().add(
            minutes=1
        ):
            response = requests.post(
                "https://accounts.spotify.com/api/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                    "client_id": spotify.CLIENT_ID,
                    "client_secret": spotify.CLIENT_SECRET,
                },
            ).json()

            self.access_token = response["access_token"]
            self.access_token_expiration = pendulum.now().add(
                seconds=response["expires_in"]
            )

        return self.access_token
