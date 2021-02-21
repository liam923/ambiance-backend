from dataclasses_json import DataClassJsonMixin
from dataclasses import dataclass

from ambiance.endpoint.endpoint import GET, endpoint
from ambiance.helpers import user_info


@dataclass
class GetUserInput(DataClassJsonMixin):
    pass


@dataclass
class GetUserOutput(DataClassJsonMixin):
    name: str
    image_url: str


@endpoint(method=GET, params=GetUserInput)
def get_user(params: GetUserInput, user: str, **kwargs) -> GetUserOutput:
    info = user_info.get_user(user)
    name = info["display_name"]
    image = info['images']['url']
    return GetUserOutput(name=name, image_url=image)
