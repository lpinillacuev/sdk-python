"""Point terminal refund intent operations."""
from mercadopago.core import MPBase


class Terminals(MPBase):
    """Manages refund intents on MercadoPago Point terminal devices."""

    def create_point_refund_intent(self, device_id, refund_intent_object,
                                   request_options=None):
        """Creates a refund intent for a payment on a terminal device.

        Args:
            device_id: Identifier of the terminal device.
            refund_intent_object: Dict with required ``payment_id`` and
                optional ``amount`` (omit for a full refund).
            request_options: Per-call configuration overrides.

        Returns:
            dict: Created refund intent, including its ID and status.
        """
        if not isinstance(refund_intent_object, dict):
            raise ValueError("Param refund_intent_object must be a Dictionary")

        return self._post(
            uri="/point/integration-api/devices/"
            + self._path_param(device_id)
            + "/refund",
            data=refund_intent_object,
            request_options=request_options,
        )

    def cancel_point_refund_intent(self, device_id, refund_intent_id,
                                   request_options=None):
        """Cancels a refund intent on a terminal device.

        Args:
            device_id: Identifier of the terminal device.
            refund_intent_id: Identifier of the refund intent to cancel.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Cancellation response and HTTP status.
        """
        return self._delete(
            uri="/point/integration-api/devices/"
            + self._path_param(device_id)
            + "/refund/"
            + self._path_param(refund_intent_id),
            request_options=request_options,
        )

    def get_point_refund_intent(self, refund_intent_id, request_options=None):
        """Retrieves a refund intent by its identifier.

        Args:
            refund_intent_id: Identifier of the refund intent.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Refund intent details and HTTP status.
        """
        return self._get(
            uri="/point/integration-api/refund/"
            + self._path_param(refund_intent_id),
            request_options=request_options,
        )

    def create_terminal_action(self, action_object, request_options=None):
        """Sends a print action to a terminal.

        Args:
            action_object: Dict with ``type``, ``external_reference``,
                ``config`` containing ``device_id``, and ``content``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Created action ID, status, and HTTP status.
        """
        if not isinstance(action_object, dict):
            raise ValueError("Param action_object must be a Dictionary")

        return self._post(
            uri="/terminals/v1/actions",
            data=action_object,
            request_options=request_options,
        )

    def get_terminal_action(self, action_id, request_options=None):
        """Retrieves the status of a terminal action.

        Args:
            action_id: Identifier of the terminal action.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Action details and HTTP status.
        """
        return self._get(
            uri="/terminals/v1/actions/" + self._path_param(action_id),
            request_options=request_options,
        )

    def cancel_terminal_action(self, action_id, request_options=None):
        """Cancels a terminal action.

        Args:
            action_id: Identifier of the terminal action.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Cancellation response and HTTP status.
        """
        return self._post(
            uri="/terminals/v1/actions/" + self._path_param(action_id) + "/cancel",
            request_options=request_options,
        )

    def update_terminal_operation_mode(self, terminal_operation_mode_object,
                                       request_options=None):
        """Updates the operating mode of one or more terminals.

        Args:
            terminal_operation_mode_object: Dict containing ``terminals`` with
                terminal ``id`` and ``operating_mode`` (PDV or STANDALONE).
            request_options: Per-call configuration overrides.

        Returns:
            dict: Operation mode update response and HTTP status.
        """
        if not isinstance(terminal_operation_mode_object, dict):
            raise ValueError("Param terminal_operation_mode_object must be a Dictionary")

        return self._patch(
            uri="/terminals/v1/setup",
            data=terminal_operation_mode_object,
            request_options=request_options,
        )

    def list_terminals(self, request_options=None):
        """Lists the terminals registered to the account.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: Registered terminals and HTTP status.
        """
        return self._get(
            uri="/terminals/v1/list",
            request_options=request_options,
        )