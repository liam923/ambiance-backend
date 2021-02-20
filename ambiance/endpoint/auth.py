import requests
from django.http import HttpResponseRedirect
from furl import furl

from ambiance.endpoint.endpoint import *
from ambiance.keys import spotify
from ambiance.model.auth_io import LoginRequest, AuthorizeRequest, State
from ambiance.model.spotify_auth import Credentials

SCOPES = " ".join(["user-library-read", "playlist-modify-private"])


@endpoint(
    method=GET, params=AuthorizeRequest, auth_required=False, unencoded_return=False
)
def authorize(params: AuthorizeRequest, **kwargs) -> HttpResponseRedirect:
    state = State.from_json(params.state)

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": params.code,
            "redirect_uri": state.spotify_redirect_uri,
            "client_id": spotify.CLIENT_ID,
            "client_secret": spotify.CLIENT_SECRET,
        },
    ).json()

    credentials = Credentials(refresh_token=response["refresh_token"], access_token=response["access_token"])

    redirect_url = furl(state.redirect_uri)
    redirect_url.args["user_token"], user_id = token.issue()
    redirect_url.args["state"] = state.given_state

    return HttpResponseRedirect(redirect_url.url)


@endpoint(method=GET, params=LoginRequest, auth_required=False, unencoded_return=False)
def login(params: LoginRequest, request_uri: str, **kwargs) -> HttpResponseRedirect:
    callback_url = furl(request_uri)
    callback_url.set(path="login/authorize")
    callback_url.set(args={})

    response_url = furl("https://accounts.spotify.com/authorize")
    response_url.set(
        args={
            "client_id": spotify.CLIENT_ID,
            "response_type": "code",
            "redirect_uri": callback_url.url,
            "state": State(
                redirect_uri=params.redirect_uri,
                spotify_redirect_uri=callback_url.url,
                given_state=params.state,
            ).to_json(separators=(",", ":")),
            "scope": SCOPES,
        }
    )

    return HttpResponseRedirect(response_url.url)
