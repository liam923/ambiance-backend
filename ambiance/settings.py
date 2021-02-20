import socket

from django.conf.urls import url
from django.http import HttpRequest, JsonResponse

from ambiance.endpoint import session, auth

DEBUG = True
SECRET_KEY = "peepeepoopoojizzjazz"
ROOT_URLCONF = __name__


def home(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"message": "Hello world."})


urlpatterns = [
    url(r"^$", home),
    url(r"login/?$", auth.login),
    url(r"login/authorize?$", auth.authorize),
    url(r"^session/create/?$", session.create),
]
