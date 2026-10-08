"""Subscription resource for the MercadoPago Subscriptions API.

Wraps ``/preapproval`` endpoints to search, retrieve, create, and update
plan-based subscriptions.  A subscription links a payer to a
:class:`~mercadopago.resources.plan.Plan` template for recurring billing.

`API reference
<https://www.mercadopago.com/developers/en/reference/online-payments/subscriptions/create-preapproval/post>`_
"""
from mercadopago.core import MPBase


class Subscription(MPBase):
    """Maps base and export Subscriptions operations to ``/preapproval``.

    HTTP mapping: ``POST /preapproval``, ``GET /preapproval/{id}``,
    ``PUT /preapproval/{id}``, ``GET /preapproval/search``, and
    ``GET /preapproval/export``. Request data and filters are passed unchanged.

    Manages plan-based recurring subscriptions.

    Each subscription is associated with a :class:`Plan` that defines
    billing frequency and amount.  Use :meth:`create` with a
    ``preapproval_plan_id`` to subscribe a payer to an existing plan.
    """

    def search(self, filters=None, request_options=None):
        """Searches subscriptions matching the given filters.

        Args:
            filters: Query-string parameters supported by
                ``searchSubscriptions``: ``q``, ``payer_id``,
                ``payer_email``, ``preapproval_plan_id``,
                ``transaction_amount``, ``semaphore``, ``status``, ``sort``,
                ``limit``, and ``offset``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Paginated list of matching subscriptions.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/subscriptions/search-preapproval/get
        """
        return self._get(
            uri="/preapproval/search",
            filters=filters,
            request_options=request_options)

    def get(self, subscription_id, request_options=None):
        """Retrieves a subscription by its ID.

        Args:
            subscription_id: Unique subscription identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Full subscription object.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/subscriptions/get-preapproval/get
        """
        return self._get(
            uri="/preapproval/" + self._path_param(subscription_id),
            request_options=request_options)

    def create(self, subscription_object, request_options=None):
        """Creates a new subscription.

        Args:
            subscription_object: Dict defining the subscription
                (preapproval_plan_id, payer_email, card_token_id, etc.).
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *subscription_object* is not a ``dict``.

        Returns:
            dict: Created subscription including its ``id`` and ``status``.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/subscriptions/create-preapproval/post
        """
        if not isinstance(subscription_object, dict):
            raise ValueError("Param subscription_object must be a Dictionary")

        return self._post(
            uri="/preapproval",
            data=subscription_object,
            request_options=request_options)

    def update(self, subscription_id, subscription_object, request_options=None):
        """Updates an existing subscription.

        Commonly used to pause, reactivate, or change the card token
        on a subscription.

        Args:
            subscription_id: Identifier of the subscription to update.
            subscription_object: Dict with the fields to modify.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *subscription_object* is not a ``dict``.

        Returns:
            dict: Updated subscription object.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/subscriptions/update-preapproval/put
        """
        if not isinstance(subscription_object, dict):
            raise ValueError("Param subscription_object must be a Dictionary")

        return self._put(
            uri="/preapproval/" + self._path_param(subscription_id),
            data=subscription_object,
            request_options=request_options)

    def export(self, filters, request_options=None):
        """Exports subscriptions as a raw CSV response.

        Args:
            filters: Query parameters containing required ``collector_id``
                and optional ``preapproval_plan_id``, ``status``, and ``sort``.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If filters is not a dictionary or ``collector_id`` is
                missing.

        Returns:
            Response: Raw HTTP response containing the CSV export payload.
        """
        if not isinstance(filters, dict):
            raise ValueError("Filters must be a Dictionary")
        if "collector_id" not in filters:
            raise ValueError("Filter collector_id is required")

        return self._get_raw(
            uri="/preapproval/export",
            filters=filters,
            request_options=request_options)
