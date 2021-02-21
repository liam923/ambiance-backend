import socket

from django.conf.urls import url
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect

from ambiance.endpoint import session, auth, playlist

DEBUG = True
SECRET_KEY = "peepeepoopoojizzjazz"
ROOT_URLCONF = __name__


def home(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"message": "Hello world."})


HttpResponseRedirect.allowed_schemes.append("exp")

urlpatterns = [
    url(r"^$", home),
    url(r"login/?$", auth.login),
    url(r"login/authorize?$", auth.authorize),
    url(r"^session/create/?$", session.create),
    url(r"^session/update/?$", session.update),
    url(r"^session/join/?$", session.join),
    url(r"^playlist/create/?$", playlist.create),

]
