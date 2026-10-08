"""Payment resource for the MercadoPago Checkout API.

Wraps ``/v1/payments`` endpoints to search, retrieve, create, update, cancel,
and capture payments.

`API reference <https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-payment/post>`_
"""
import warnings

from mercadopago.core import MPBase
from mercadopago.pagination.iterator import search_auto_paging_iter as _paging_iter


class Payment(MPBase):
    """Manages payment lifecycle through the MercadoPago Checkout API.

    Supports transparent (server-to-server) payments as well as payments
    originated from Checkout Pro / Checkout Bricks.

    `Integration guide
    <https://www.mercadopago.com.br/developers/en/guides/online-payments/checkout-api/introduction/>`_
    """

    def search(self, filters=None, request_options=None):
        """Searches payments matching the given filters.

        Args:
            filters: Query-string parameters documented by the search API,
                including ``sort``, ``criteria``, date ranges, status, store,
                point-of-sale, collector/payer IDs, limit, and offset.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Paginated list of matching payments.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/search-payments/get
        """
        return self._get(uri="/v1/payments/search", filters=filters,
                         request_options=request_options)

    def get(self, payment_id, request_options=None):
        """Retrieves a single payment by its ID.

        Args:
            payment_id: Numeric or string payment identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Full payment object.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/get-payment/get
        """
        return self._get(
            uri="/v1/payments/" + self._path_param(payment_id),
            request_options=request_options,
        )

    def create(self, payment_object, request_options=None):
        """Creates a new payment.

        Args:
            payment_object: Generic dict containing the documented payment
                request fields.
            request_options: Per-call configuration overrides, including an
                optional ``X-Idempotency-Key`` custom header.

        Raises:
            ValueError: If *payment_object* is not a ``dict``.

        Returns:
            dict: Created payment including its ``id`` and ``status``.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-payment/post
        """
        if not isinstance(payment_object, dict):
            raise ValueError("Param payment_object must be a Dictionary")
        if "notification_url" in payment_object:
            warnings.warn(
                "notification_url is deprecated; use Webhooks instead. "
                "See https://www.mercadopago.com/developers/en/docs/your-integrations/notifications/webhooks",
                DeprecationWarning,
                stacklevel=2,
            )
        return self._post(
            uri="/v1/payments",
            data=payment_object,
            request_options=request_options,
        )

    def update(self, payment_id, payment_object, request_options=None):
        """Updates or captures an existing payment.

        The generic dictionary body supports the documented update fields,
        including ``capture``, ``status``, ``transaction_amount``, and
        ``date_of_expiration``.

        Args:
            payment_id: Identifier of the payment to update.
            payment_object: Generic dict with the fields to modify.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *payment_object* is not a ``dict``.

        Returns:
            dict: Updated payment object.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/update-payment/put
        """
        if not isinstance(payment_object, dict):
            raise ValueError("Param payment_object must be a Dictionary")

        return self._put(
            uri="/v1/payments/" + self._path_param(payment_id),
            data=payment_object,
            request_options=request_options,
        )

    def cancel(self, payment_id, request_options=None):
        """Cancels a pending or authorized payment through its dedicated endpoint.

        Args:
            payment_id: Identifier of the payment to cancel.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Cancelled payment object.

        Reference: PUT /v1/payments/{id}/cancellations
        """
        return self._put(
            uri=(
                "/v1/payments/"
                + self._path_param(payment_id)
                + "/cancellations"
            ),
            data={"status": "cancelled"},
            request_options=request_options,
        )

    def capture(self, payment_id, amount=None, request_options=None):
        """Captures an authorized payment.

        Args:
            payment_id: Identifier of the authorized payment to capture.
            amount: Amount to capture. If ``None``, the full authorized amount
                is captured.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Updated payment object reflecting the captured state.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/update-payment/put
        """
        payload = {"capture": True}
        if amount is not None:
            payload["transaction_amount"] = amount
        return self.update(
            payment_id,
            payload,
            request_options=request_options,
        )

    def search_auto_paging_iter(self, filters=None, request_options=None, limit=100):
        """Lazily yields every payment matching *filters* across all pages.

        Args:
            filters: Search criteria (e.g. ``{"status": "approved"}``).
            request_options: Per-call configuration overrides.
            limit: Items per page. Defaults to 100.

        Yields:
            dict: Individual payment objects.
        """
        return _paging_iter(self.search, filters, request_options, limit)