from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json
from django.http import JsonResponse


@dataclass_json
@dataclass
class ErrorMessage:
    message: str


@dataclass_json
@dataclass
class Error(Exception):
    status_code: int
    message: Optional[ErrorMessage] = None

    def as_response(self) -> JsonResponse:
        message = self.message or ErrorMessage(f"A {self.status_code} error occurred")
        return JsonResponse(message.to_dict(), status=self.status_code)
