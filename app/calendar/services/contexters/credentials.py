from datetime import datetime, timedelta

from django.conf import settings
from google.oauth2.credentials import Credentials
from social_django.models import UserSocialAuth


class CredentialsContexter:
    class Context:
        def __init__(
            self, contexter: 'CredentialsContexter', social_auth: UserSocialAuth
        ):
            self.contexter = contexter
            self.social_auth = social_auth
            self.credentials = contexter.create_credentials(social_auth)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if (
                self.contexter.extract_expiry(self.social_auth)
                != self.credentials.expiry
            ):
                self.contexter._refresh_social_auth(
                    credentials=self.credentials, social_auth=self.social_auth
                )
            return False

    def __init__(
        self,
        client_id: str = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        client_secret: str = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        token_uri: str = 'https://oauth2.googleapis.com/token',
        default_expires: timedelta = timedelta(seconds=3599),
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_uri = token_uri
        self.default_expires = default_expires

    def extract_expiry(self, social_auth: UserSocialAuth) -> datetime:
        return datetime.fromtimestamp(
            social_auth.extra_data['auth_time'] + social_auth.extra_data['expires']
        )

    def create_credentials(self, social_auth: UserSocialAuth) -> Credentials:
        extra_data = social_auth.extra_data
        return Credentials(
            token=extra_data['access_token'],
            refresh_token=extra_data['refresh_token'],
            token_uri=self.token_uri,
            client_id=self.client_id,
            client_secret=self.client_secret,
            expiry=self.extract_expiry(social_auth),
        )

    def create_context(self, social_auth: UserSocialAuth) -> Context:
        return self.Context(self, social_auth)

    def _refresh_social_auth(
        self, credentials: Credentials, social_auth: UserSocialAuth
    ) -> None:
        social_auth.extra_data['access_token'] = credentials.token
        social_auth.extra_data['expires'] = self.default_expires.seconds
        social_auth.extra_data['auth_time'] = int(
            (credentials.expiry - self.default_expires).timestamp()
        )
        social_auth.save(update_fields=['extra_data'])
