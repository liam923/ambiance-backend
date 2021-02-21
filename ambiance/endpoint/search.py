from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin
from django.http import JsonResponse

from ambiance.endpoint.endpoint import endpoint, GET
from ambiance.helpers import search_helper


@dataclass
class SearchInput(DataClassJsonMixin):
    query: str


@dataclass
class SearchOutput(DataClassJsonMixin):
    response: JsonResponse


@endpoint(method=GET, params=SearchInput)
def search(params: SearchInput, user: str, **kwargs) -> SearchOutput:
    res = search_helper.search(params.query, user)
    return SearchOutput(res)
