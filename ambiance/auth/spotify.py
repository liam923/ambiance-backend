from spotipy import SpotifyOAuth


class SpotifyAuthManager:
    def __init__(self):
        self.auth = SpotifyOAuth(client_id="", client_secret="",
                                 redirect_uri="https://google.com", open_browser=False)
        self.auth.get_authorize_url()
        self.refresh_token = ""
        self.current_token = None

    def get_access_token(self):
        import datetime
        now = datetime.datetime.now()

        # if no token or token about to expire soon
        if not self.current_token or self.current_token['expires_at'] > now.timestamp() + 60:
            self.current_token = self.auth.refresh_access_token(self.refresh_token)

        return self.current_token['access_token']
