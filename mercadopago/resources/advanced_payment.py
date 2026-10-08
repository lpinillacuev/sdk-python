"""Advanced Payment resource for the MercadoPago Marketplace API.

Wraps ``/v1/advanced_payments`` endpoints used in marketplace split-payment
scenarios where funds are distributed among multiple receivers.

`API reference <https://www.mercadopago.com/developers/en/reference>`_
(advanced_payments section not found in current reference)
"""
from datetime import datetime

from mercadopago.core import MPBase


class AdvancedPayment(MPBase):
    """Manages split payments in marketplace integrations.

    Advanced payments allow a marketplace to collect a payment and split
    it among multiple sellers in a single transaction.  Supports
    two-step flows (authorise then capture) and individual disbursement
    release-date control.
    """

    def create_wallet_agreement(self, agreement_object, filters=None,
                                request_options=None):
        """Creates a Wallet Connect agreement."""
        if not isinstance(agreement_object, dict):
            raise ValueError("Param agreement_object must be a Dictionary")

        return self._post(
            uri="/v2/wallet_connect/agreements",
            data=agreement_object,
            params=filters,
            request_options=request_options,
        )

    def get_wallet_agreement(self, agreement_id, filters=None,
                             request_options=None):
        """Retrieves a Wallet Connect agreement."""
        return self._get(
            uri="/v2/wallet_connect/agreements/"
            + self._path_param(agreement_id),
            filters=filters,
            request_options=request_options,
        )

    def delete_wallet_agreement(self, agreement_id, filters=None,
                                request_options=None):
        """Revokes a Wallet Connect agreement."""
        return self._delete(
            uri="/v2/wallet_connect/agreements/"
            + self._path_param(agreement_id),
            params=filters,
            request_options=request_options,
        )

    def create_wallet_payer_token(self, agreement_id, token_object,
                                  request_options=None):
        """Creates a payer token from a Wallet Connect agreement."""
        if not isinstance(token_object, dict):
            raise ValueError("Param token_object must be a Dictionary")

        return self._post(
            uri="/v2/wallet_connect/agreements/"
            + self._path_param(agreement_id)
            + "/payer_token",
            data=token_object,
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

    def get(self, advanced_payment_id, request_options=None):
        """Retrieves an advanced payment by its ID.

        Args:
            advanced_payment_id: Unique advanced payment identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Full advanced payment object.
        """
        return self._get(uri="/v1/advanced_payments/" + self._path_param(advanced_payment_id),
                         request_options=request_options)

    def create(self, advanced_payment_object, request_options=None):
        """Creates a new advanced (split) payment.

        Args:
            advanced_payment_object: Dict describing the payment including
                ``disbursements`` (list of receiver/amount pairs).
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *advanced_payment_object* is not a ``dict``.

        Returns:
            dict: Created advanced payment including its ``id``.
        """
        if not isinstance(advanced_payment_object, dict):
            raise ValueError(
                "Param advanced_payment_object must be a Dictionary")

        return self._post(uri="/v1/advanced_payments", data=advanced_payment_object,
                          request_options=request_options)

    def capture(self, advanced_payment_id, request_options=None):
        """Captures a previously authorised advanced payment.

        Sends ``{"capture": true}`` to finalise a two-step payment flow.

        Args:
            advanced_payment_id: Identifier of the payment to capture.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Captured advanced payment with updated status.
        """
        capture_object = {"capture": True}
        return self._put(uri="/v1/advanced_payments/" + self._path_param(advanced_payment_id),
                         data=capture_object, request_options=request_options)

    def update(self, advanced_payment_id, advanced_payment_object, request_options=None):
        """Updates an existing advanced payment.

        Args:
            advanced_payment_id: Identifier of the payment to update.
            advanced_payment_object: Dict with the fields to modify.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *advanced_payment_object* is not a ``dict``.

        Returns:
            dict: Updated advanced payment object.
        """
        if not isinstance(advanced_payment_object, dict):
            raise ValueError(
                "Param advanced_payment_object must be a Dictionary")

        return self._put(uri="/v1/advanced_payments/" + self._path_param(advanced_payment_id),
                         data=advanced_payment_object, request_options=request_options)

    def cancel(self, advanced_payment_id, request_options=None):
        """Cancels an advanced payment.

        Sets the payment status to ``cancelled``.  Only payments that
        have not yet been captured can be cancelled.

        Args:
            advanced_payment_id: Identifier of the payment to cancel.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Cancelled advanced payment with updated status.
        """
        cancel_object = {"status": "cancelled"}
        return self._put(uri="/v1/advanced_payments/" + self._path_param(advanced_payment_id),
                         data=cancel_object, request_options=request_options)

    def update_release_date(self, advanced_payment_id, release_date, request_options=None):
        """Changes the money release date for disbursements.

        Allows the marketplace to control when funds become available
        to sellers.

        Args:
            advanced_payment_id: Identifier of the advanced payment.
            release_date: New release ``datetime`` for the disbursements.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *release_date* is not a ``datetime`` instance.

        Returns:
            dict: Updated disbursement schedule response.
        """
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
