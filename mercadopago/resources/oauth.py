"""OAuth resource for the MercadoPago Authorization API.

Wraps the unauthenticated ``POST /oauth/token`` operation used to exchange
OAuth grants for access and refresh tokens.
"""
from urllib.parse import urlencode

from mercadopago.core import MPBase


_AUTH_URL = "https://auth.mercadopago.com/authorization"


class OAuth(MPBase):
    """Manages the OAuth 2.0 authorization and token flows."""

    def get_authorization_url(self, app_id, redirect_uri, random_id):
        """Builds the authorization URL, including the CSRF state value."""
        params = {
            "client_id": app_id,
            "response_type": "code",
            "platform_id": "mp",
            "state": random_id,
            "redirect_uri": redirect_uri,
        }
        return _AUTH_URL + "?" + urlencode(params)

    def create(self, oauth_object, request_options=None):
        """Creates a token from an OAuth request body without bearer auth."""
        if not isinstance(oauth_object, dict):
            raise ValueError("Param oauth_object must be a Dictionary")

        return self._post(
            uri="/oauth/token",
            data=oauth_object,
            request_options=request_options,
            authenticated=False,
        )

    def refresh(self, oauth_object, request_options=None):
        """Refreshes a token using the unauthenticated token operation."""
        if not isinstance(oauth_object, dict):
            raise ValueError("Param oauth_object must be a Dictionary")

        return self._post(
            uri="/oauth/token",
            data=oauth_object,
            request_options=request_options,
            authenticated=False,
        )