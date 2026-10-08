"""Point and Terminals resources for in-person payment operations.

Wraps the deprecated ``/point/integration-api`` payment-intent API and the
current terminal, refund-intent, and print-action endpoints.
"""
from mercadopago.core import MPBase


class Point(MPBase):
    """Manages payment intents on MercadoPago Point (POS) devices.

    Enables in-person payment processing by creating payment intents
    that are sent to a physical Point device for the buyer to complete
    the transaction by inserting or tapping their card.
    """

    @staticmethod
    def _require_dict(value, name):
        if not isinstance(value, dict):
            raise ValueError("Param " + name + " must be a Dictionary")

    def get_devices(self, filters=None, request_options=None):
        """Lists Point devices linked to the authenticated account.

        Args:
            filters: Optional query-string parameters such as
                ``store_id`` and ``pos_id``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: List of devices with their identifiers, operating
                modes, and statuses.

        Reference: https://www.mercadopago.com/developers/en/reference/in-person-payments/point/devices/list-devices/get
        """
        return self._get(
            uri="/point/integration-api/devices",
            filters=filters,
            request_options=request_options,
        )

    def create(self, device_id, payment_intent_object, request_options=None):
        """Creates a payment intent on a specific Point device.

        The payment intent is sent to the physical device, where the
        buyer completes the transaction.

        Args:
            device_id: Unique identifier of the target Point device.
            payment_intent_object: Dict describing the payment intent,
                including ``amount``, ``description``, and ``payment``
                method details.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *payment_intent_object* is not a ``dict``.

        Returns:
            dict: Created payment intent including its ``id`` and
                ``state``.

        Reference: https://www.mercadopago.com/developers/en/reference/in-person-payments/point/orders/create-order/post
        """
        if not isinstance(payment_intent_object, dict):
            raise ValueError("Param payment_intent_object must be a Dictionary")

        return self._post(
            uri="/point/integration-api/devices/"
            + self._path_param(device_id)
            + "/payment-intents",
            data=payment_intent_object,
            request_options=request_options,
        )

    def get(self, payment_intent_id, request_options=None):
        """Retrieves the current state of a payment intent by its ID.

        Use this to check whether the buyer has completed, cancelled,
        or is still processing the payment on the device.

        Args:
            payment_intent_id: Unique identifier of the payment intent.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Payment intent details including its ``state`` and,
                when completed, the associated ``payment_id``.

        Reference: https://www.mercadopago.com/developers/en/reference/in-person-payments/point/orders/get-order/get
        """
        return self._get(
            uri="/point/integration-api/payment-intents/" + self._path_param(payment_intent_id),
            request_options=request_options,
        )

    def cancel(self, device_id, payment_intent_id, request_options=None):
        """Cancels a pending payment intent on a specific device.

        Use this to abort a transaction before the buyer completes the
        payment on the device.

        Args:
            device_id: Unique identifier of the Point device holding
                the intent.
            payment_intent_id: Unique identifier of the payment intent
                to cancel.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Cancellation confirmation.

        Reference: https://www.mercadopago.com/developers/en/reference/in-person-payments/point/orders/cancel-order/post
        """
        return self._delete(
            uri="/point/integration-api/devices/" + self._path_param(device_id)
                + "/payment-intents/" + self._path_param(payment_intent_id),
            request_options=request_options,
        )


class Terminals(MPBase):
    """Manages Point terminals, refund intents, and print actions."""

    @staticmethod
    def _require_dict(value, name):
        if not isinstance(value, dict):
            raise ValueError("Param " + name + " must be a Dictionary")

    def list(self, request_options=None):
        """Lists terminals linked to the authenticated account."""
        return self._get(
            uri="/terminals/v1/list",
            request_options=request_options,
        )

    def update_operation_mode(self, setup_object, request_options=None):
        """Updates the operating mode of one or more terminals."""
        self._require_dict(setup_object, "setup_object")
        return self._patch(
            uri="/terminals/v1/setup",
            data=setup_object,
            request_options=request_options,
        )

    def create_refund(self, device_id, refund_object, request_options=None):
        """Creates a refund intent on a terminal."""
        self._require_dict(refund_object, "refund_object")
        return self._post(
            uri="/point/integration-api/devices/"
            + self._path_param(device_id)
            + "/refund",
            data=refund_object,
            request_options=request_options,
        )

    def cancel_refund(self, device_id, refund_intent_id, request_options=None):
        """Cancels a refund intent on a terminal."""
        return self._delete(
            uri="/point/integration-api/devices/"
            + self._path_param(device_id)
            + "/refund/"
            + self._path_param(refund_intent_id),
            request_options=request_options,
        )

    def get_refund(self, refund_intent_id, request_options=None):
        """Gets a refund intent by identifier."""
        return self._get(
            uri="/point/integration-api/refund/"
            + self._path_param(refund_intent_id),
            request_options=request_options,
        )

    def create_action(self, action_object, request_options=None):
        """Creates a terminal print action."""
        self._require_dict(action_object, "action_object")
        return self._post(
            uri="/terminals/v1/actions",
            data=action_object,
            request_options=request_options,
        )

    def get_action(self, action_id, request_options=None):
        """Gets a terminal action by identifier."""
        return self._get(
            uri="/terminals/v1/actions/" + self._path_param(action_id),
            request_options=request_options,
        )

    def cancel_action(self, action_id, request_options=None):
        """Cancels a terminal action."""
        return self._post(
            uri="/terminals/v1/actions/"
            + self._path_param(action_id)
            + "/cancel",
            request_options=request_options,
        )
