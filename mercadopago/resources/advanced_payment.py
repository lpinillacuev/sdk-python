"""Advanced payments and Wallet Connect resource.

Wraps the advanced payment and Wallet Connect agreement, payer-token,
discount, and coupon endpoints.
"""
from datetime import datetime

from mercadopago.core import MPBase


class AdvancedPayment(MPBase):
    """Manages advanced payments and Wallet Connect operations."""

    ADVANCED_PAYMENTS_URI = "/v1/advanced_payments"
    WALLET_AGREEMENTS_URI = "/v2/wallet_connect/agreements"
    WALLET_DISCOUNTS_URI = "/v2/wallet_connect/discounts"
    WALLET_COUPONS_URI = "/v2/wallet_connect/coupons"

    def search(self, filters=None, request_options=None):
        return self._get(
            uri="/v1/advanced_payments/search",
            filters=filters,
            request_options=request_options,
        )

    def get(self, advanced_payment_id, request_options=None):
        return self._get(
            uri="/v1/advanced_payments/" + self._path_param(advanced_payment_id),
            request_options=request_options,
        )

    def create(self, advanced_payment_object, request_options=None):
        if not isinstance(advanced_payment_object, dict):
            raise ValueError(
                "Param advanced_payment_object must be a Dictionary")

        return self._post(
            uri="/v1/advanced_payments",
            data=advanced_payment_object,
            request_options=request_options,
        )

    def capture(self, advanced_payment_id, request_options=None):
        return self.update(
            advanced_payment_id, {"capture": True}, request_options)

    def update(self, advanced_payment_id, advanced_payment_object,
               request_options=None):
        if not isinstance(advanced_payment_object, dict):
            raise ValueError(
                "Param advanced_payment_object must be a Dictionary")

        return self._put(
            uri="/v1/advanced_payments/" + self._path_param(advanced_payment_id),
            data=advanced_payment_object,
            request_options=request_options,
        )

    def cancel(self, advanced_payment_id, request_options=None):
        return self.update(
            advanced_payment_id, {"status": "cancelled"}, request_options)

    def create_wallet_agreement(self, agreement_object, client_id=None,
                                request_options=None):
        """Creates a Wallet Connect agreement."""
        if not isinstance(agreement_object, dict):
            raise ValueError("Param agreement_object must be a Dictionary")
        params = {"client.id": client_id} if client_id is not None else None
        return self._post(
            uri="/v2/wallet_connect/agreements",
            data=agreement_object,
            params=params,
            request_options=request_options,
        )

    def get_wallet_agreement(self, agreement_id, client_id=None,
                             request_options=None):
        """Retrieves a Wallet Connect agreement."""
        filters = {"client.id": client_id} if client_id is not None else None
        return self._get(
            uri="/v2/wallet_connect/agreements/"
            + self._path_param(agreement_id),
            filters=filters,
            request_options=request_options,
        )

    def delete_wallet_agreement(self, agreement_id, client_id=None,
                                request_options=None):
        """Revokes a Wallet Connect agreement."""
        params = {"client.id": client_id} if client_id is not None else None
        return self._delete(
            uri="/v2/wallet_connect/agreements/"
            + self._path_param(agreement_id),
            params=params,
            request_options=request_options,
        )

    def create_wallet_payer_token(self, agreement_id, payer_token_object,
                                  request_options=None):
        """Creates a payer token from a Wallet Connect agreement."""
        if not isinstance(payer_token_object, dict):
            raise ValueError("Param payer_token_object must be a Dictionary")
        return self._post(
            uri="/v2/wallet_connect/agreements/"
            + self._path_param(agreement_id)
            + "/payer_token",
            data=payer_token_object,
            request_options=request_options,
        )

    def create_wallet_discount(self, discount_object, request_options=None):
        """Creates a Wallet Connect discount promise."""
        if not isinstance(discount_object, dict):
            raise ValueError("Param discount_object must be a Dictionary")
        return self._post(
            uri="/v2/wallet_connect/discounts",
            data=discount_object,
            request_options=request_options,
        )

    def validate_wallet_coupon(self, coupon_object, request_options=None):
        """Validates a Wallet Connect coupon."""
        if not isinstance(coupon_object, dict):
            raise ValueError("Param coupon_object must be a Dictionary")
        return self._post(
            uri="/v2/wallet_connect/coupons",
            data=coupon_object,
            request_options=request_options,
        )

    def update_release_date(self, advanced_payment_id, release_date,
                            request_options=None):
        if not isinstance(release_date, datetime):
            raise ValueError("Param release_date must be a DateTime")

        disbursement_object = {
            "money_release_date": release_date.strftime("%Y-%m-%d %H:%M:%S.%f")}

        return self._post(
            uri="/v1/advanced_payments/"
            + self._path_param(advanced_payment_id)
            + "/disburses",
            data=disbursement_object,
            request_options=request_options,
        )