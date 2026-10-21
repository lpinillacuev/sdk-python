"""Wallet Connect resource for creating and managing authorization agreements."""
from copy import copy

from mercadopago.core import MPBase


class WalletConnect(MPBase):
    """Manages Wallet Connect agreements and payer tokens."""

    def __init__(self, request_options, http_client):
        MPBase.__init__(self, request_options, http_client)

    def create_wallet_agreement(self, agreement_object, client_id=None,
                                request_options=None):
        """Creates a Wallet Connect authorization agreement.

        Args:
            agreement_object: Agreement request body, including return_uri
                and external_flow_id.
            client_id: Optional client.id query parameter.
            request_options: Per-call options, including optional platform_id
                for the x-platform-id header.

        Returns:
            dict: HTTP status and created agreement details.
        """
        if not isinstance(agreement_object, dict):
            raise ValueError("Param agreement_object must be a Dictionary")

        params = {"client.id": client_id} if client_id is not None else None
        return self._post(uri="/v2/wallet_connect/agreements",
                          data=agreement_object, params=params,
                          request_options=request_options)

    def delete_wallet_agreement(self, agreement_id, client_id=None,
                                request_options=None):
        """Revokes a Wallet Connect agreement.

        Args:
            agreement_id: Agreement identifier.
            client_id: Optional client.id query parameter.
            request_options: Per-call options, including optional platform_id
                for the x-platform-id header.

        Returns:
            dict: HTTP status and API response.
        """
        params = {"client.id": client_id} if client_id is not None else None
        return self._delete(
            uri="/v2/wallet_connect/agreements/" + self._path_param(agreement_id),
            params=params, request_options=request_options)

    def get_wallet_agreement(self, agreement_id, client_id=None,
                             request_options=None):
        """Retrieves a Wallet Connect agreement.

        Args:
            agreement_id: Agreement identifier.
            client_id: Optional client.id query parameter.
            request_options: Per-call options, including optional platform_id
                for the x-platform-id header.

        Returns:
            dict: HTTP status and agreement details.
        """
        filters = {"client.id": client_id} if client_id is not None else None
        return self._get(
            uri="/v2/wallet_connect/agreements/" + self._path_param(agreement_id),
            filters=filters, request_options=request_options)

    def create_wallet_payer_token(self, agreement_id, payer_token_object,
                                  request_options=None):
        """Creates a payer token from an agreement authorization code.

        Args:
            agreement_id: Agreement identifier.
            payer_token_object: Request body containing the authorization code.
            request_options: Per-call options, including optional platform_id
                for the x-platform-id header.

        Returns:
            dict: HTTP status and payer token.
        """
        if not isinstance(payer_token_object, dict):
            raise ValueError("Param payer_token_object must be a Dictionary")

        return self._post(
            uri="/v2/wallet_connect/agreements/" +
            self._path_param(agreement_id) + "/payer_token",
            data=payer_token_object, request_options=request_options)

    def validate_wallet_coupon(self, coupon_object, payer_token,
                               request_options=None):
        """Validates a Wallet Connect coupon.

        Args:
            coupon_object: Request body containing the coupon id.
            payer_token: Payer wallet token sent in the x-payer-token header.
            request_options: Optional per-call request options.

        Returns:
            dict: HTTP status and coupon validation details.
        """
        if not isinstance(coupon_object, dict):
            raise ValueError("Param coupon_object must be a Dictionary")

        options = copy(request_options if request_options is not None
                       else self.request_options)
        headers = dict(options.custom_headers or {})
        headers["x-payer-token"] = payer_token
        options.custom_headers = headers
        return self._post(uri="/v2/wallet_connect/coupons",
                          data=coupon_object, request_options=options)

    def create_wallet_discount(self, discount_object, payer_token,
                               request_options=None):
        """Creates a Wallet Connect discount promise.

        Args:
            discount_object: Request body containing coupon and amount.
            payer_token: Payer wallet token sent in the x-payer-token header.
            request_options: Optional per-call request options.

        Returns:
            dict: HTTP status and discount details.
        """
        if not isinstance(discount_object, dict):
            raise ValueError("Param discount_object must be a Dictionary")

        options = copy(request_options if request_options is not None
                       else self.request_options)
        headers = dict(options.custom_headers or {})
        headers["x-payer-token"] = payer_token
        options.custom_headers = headers
        return self._post(uri="/v2/wallet_connect/discounts",
                          data=discount_object, request_options=options)
