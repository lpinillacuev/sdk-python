"""Card-token endpoint mappings for the MercadoPago API.

Token creation accepts the generic ``CardTokenRequest`` dictionary for SDK
compatibility. It is a public-key, client-side-only operation: integrations
must use MercadoPago.js or Secure Fields so raw PAN and CVV never traverse the
application backend. Token retrieval remains a bearer-authenticated operation.
"""
from mercadopago.core import MPBase


class CardToken(MPBase):
    """Retrieves card tokens and exposes the client-side tokenization mapping."""

    def get(self, card_token_id, request_options=None):
        """Gets token metadata by ID using bearer authentication."""
        return self._get(
            uri=f"/v1/card_tokens/{self._path_param(card_token_id)}",
            request_options=request_options,
        )

    def create(self, card_token_object, request_options=None):
        """Maps client-side card-token creation.

        This operation requires a public key rather than a server access token.
        Backend applications must not use it with raw card data; use
        MercadoPago.js or Secure Fields in the browser instead.
        """
        if not isinstance(card_token_object, dict):
            raise ValueError("Param card_token_object must be a Dictionary")

        return self._post(
            uri="/v1/card_tokens",
            data=card_token_object,
            request_options=request_options,
        )