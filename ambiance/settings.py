import socket

from django.conf.urls import url
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect

import ambiance.endpoint.session as session
import ambiance.endpoint.auth as auth
import ambiance.endpoint.playlist as playlist
import ambiance.endpoint.user_info as user_info
import ambiance.endpoint.jukebox as jukebox
from ambiance.endpoint import search

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
    url(r"^user/info/?$", user_info.get_user),
    url(r"^jukebox/start/?$", jukebox.start),
    url(r"^jukebox/stop/?$", jukebox.stop),
    url(r"^spotify/search/?$", search.search),
]
