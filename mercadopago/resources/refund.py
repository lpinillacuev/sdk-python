"""Refund resource for the MercadoPago Payments API.

Wraps ``/v1/payments/{id}/refunds`` and
``/v1/payments/{id}/refunds/{refund_id}`` endpoints to create, list, and
retrieve refunds on approved payments.

Refunds are available within 180 days of payment approval and require
sufficient account balance.

`API reference <https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-refund/post>`_
"""
from mercadopago.core import MPBase


class Refund(MPBase):
    """Creates and lists refunds for payments.

    Supports full refunds (omit *refund_object*) and partial refunds
    (pass ``{"amount": <float>}``).  Refunds can only be issued for
    approved payments within 180 days.
    """

    def list_all(self, payment_id, request_options=None):
        """Lists all refunds issued for a payment.

        Args:
            payment_id: Identifier of the parent payment.
            request_options: Per-call configuration overrides.

        Returns:
            dict: List of refund objects.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/get-refunds/get
        """
        return self._get(
            uri=f"/v1/payments/{self._path_param(payment_id)}/refunds",
            request_options=request_options,
        )

    def create(self, payment_id, refund_request=None, request_options=None):
        """Creates a refund for a payment.

        Omit *refund_request* for a full refund, or pass a ``RefundRequest``
        dictionary such as ``{"amount": <float>}`` for a partial refund.

        Args:
            payment_id: Identifier of the payment to refund.
            refund_request: Optional RefundRequest dictionary.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *refund_request* is provided but not a ``dict``.

        Returns:
            dict: Created refund including its ``id`` and ``status``.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-refund/post
        """
        if refund_request is not None and not isinstance(refund_request, dict):
            raise ValueError("Param refund_request must be a Dictionary")

        return self._post(
            uri=f"/v1/payments/{self._path_param(payment_id)}/refunds",
            data=refund_request,
            request_options=request_options,
        )

    def get(self, payment_id, refund_id, request_options=None):
        """Retrieves a single refund by its ID.

        Args:
            payment_id: Identifier of the parent payment.
            refund_id: Identifier of the refund to retrieve.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Refund object including its ``id`` and ``status``.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/get-refund/get
        """
        return self._get(
            uri=f"/v1/payments/{self._path_param(payment_id)}"
                f"/refunds/{self._path_param(refund_id)}",
            request_options=request_options,
        )
