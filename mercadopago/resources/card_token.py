"""Card Token resource for the MercadoPago API.

Card token creation is exposed for API compatibility but requires a public key.
Use MercadoPago.js or MP Secure Fields in client-side applications so raw card
PAN and CVV do not pass through your server.
"""
from mercadopago.core import MPBase


class CardToken(MPBase):
    """Creates card tokens with a public key and retrieves token metadata."""

    def create(self, card_token_object, request_options=None):
        """Creates a card token using ``X-Public-Key`` authentication.

        Callers must provide a ``RequestOptions`` whose custom headers include
        ``X-Public-Key``. Client-side tokenization remains the recommended flow.

        Args:
            card_token_object: Card token request body.
            request_options: Per-call options containing the public-key header.

        Returns:
            dict: Created card token response.
        """
        if not isinstance(card_token_object, dict):
            raise ValueError("card_token_object must be a Dictionary")
        custom_headers = getattr(request_options, "custom_headers", None) or {}
        public_key = next(
            (value for name, value in custom_headers.items()
             if name.lower() == "x-public-key"),
            None,
        )
        if not public_key:
            raise ValueError(
                "CardToken.create requires RequestOptions with an X-Public-Key header"
            )

        return self._post(
            uri="/v1/card_tokens",
            data=card_token_object,
            request_options=request_options,
            use_access_token=False,
        )

    def get(self, card_token_id, request_options=None):
        """Retrieves a card token by its ID.

        Args:
            card_token_id: Unique token identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Token metadata (last four digits, expiry, etc.).
        """
        return self._get(uri="/v1/card_tokens/" + self._path_param(card_token_id),
                         request_options=request_options)