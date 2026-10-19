"""Wallet Connect agreements, payer tokens, coupons, and discounts."""
from copy import copy

from mercadopago.core import MPBase


class WalletConnect(MPBase):
    """Access the Wallet Connect API through the SDK's HTTP client."""

    def _wallet_options(self, request_options, platform_id=None, payer_token=None):
        """Add operation-specific headers without changing caller defaults."""
        if platform_id is None and payer_token is None:
            return request_options
        options = copy(request_options if request_options is not None else self.request_options)
        if platform_id is not None:
            options.platform_id = platform_id
        if payer_token is not None:
            headers = dict(options.custom_headers or {})
            headers["x-payer-token"] = payer_token
            options.custom_headers = headers
        return options

    def create_wallet_agreement(self, agreement_object, client_id=None,
                                platform_id=None, request_options=None):
        """Create a Wallet Connect agreement using a JSON request body."""
        if not isinstance(agreement_object, dict):
            raise ValueError("Param agreement_object must be a Dictionary")
        params = {"client.id": client_id} if client_id is not None else None
        return self._post(
            uri="/v2/wallet_connect/agreements",
            data=agreement_object,
            params=params,
            request_options=self._wallet_options(request_options, platform_id),
        )

    def delete_wallet_agreement(self, agreement_id, client_id=None,
                                platform_id=None, request_options=None):
        """Revoke an agreement by its safely encoded ID."""
        if not isinstance(agreement_id, str):
            raise ValueError("Param agreement_id must be a string")
        params = {"client.id": client_id} if client_id is not None else None
        return self._delete(
            uri="/v2/wallet_connect/agreements/" + self._path_param(agreement_id),
            params=params,
            request_options=self._wallet_options(request_options, platform_id),
        )

    def get_wallet_agreement(self, agreement_id, client_id=None,
                             platform_id=None, request_options=None):
        """Retrieve an agreement by its safely encoded ID."""
        if not isinstance(agreement_id, str):
            raise ValueError("Param agreement_id must be a string")
        filters = {"client.id": client_id} if client_id is not None else None
        return self._get(
            uri="/v2/wallet_connect/agreements/" + self._path_param(agreement_id),
            filters=filters,
            request_options=self._wallet_options(request_options, platform_id),
        )

    def create_wallet_payer_token(self, agreement_id, token_object,
                                  platform_id=None, request_options=None):
        """Exchange the authorization code in the JSON body for a payer token."""
        if not isinstance(agreement_id, str):
            raise ValueError("Param agreement_id must be a string")
        if not isinstance(token_object, dict):
            raise ValueError("Param token_object must be a Dictionary")
        return self._post(
            uri="/v2/wallet_connect/agreements/"
            + self._path_param(agreement_id) + "/payer_token",
            data=token_object,
            request_options=self._wallet_options(request_options, platform_id),
        )

    def validate_wallet_coupon(self, coupon_object, payer_token, request_options=None):
        """Validate a coupon ID in the body using the payer token header."""
        if not isinstance(coupon_object, dict):
            raise ValueError("Param coupon_object must be a Dictionary")
        if not isinstance(payer_token, str):
            raise ValueError("Param payer_token must be a string")
        return self._post(
            uri="/v2/wallet_connect/coupons",
            data=coupon_object,
            request_options=self._wallet_options(request_options, payer_token=payer_token),
        )

    def create_wallet_discount(self, discount_object, payer_token, request_options=None):
        """Create a discount from coupon and amount in the JSON body."""
        if not isinstance(discount_object, dict):
            raise ValueError("Param discount_object must be a Dictionary")
        if not isinstance(payer_token, str):
            raise ValueError("Param payer_token must be a string")
        return self._post(
            uri="/v2/wallet_connect/discounts",
            data=discount_object,
            request_options=self._wallet_options(request_options, payer_token=payer_token),
        )