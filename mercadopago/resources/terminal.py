"""Terminal actions and terminal listing for the Mercado Pago API."""
from mercadopago.core import MPBase


class Terminal(MPBase):
    """Manages print actions and lists registered Point terminals."""

    def create_action(self, action_object, request_options=None):
        """Send a print action to a terminal."""
        if not isinstance(action_object, dict):
            raise ValueError("Param action_object must be a Dictionary")
        return self._post(
            uri="/terminals/v1/actions",
            data=action_object,
            request_options=request_options,
        )

    def get_action(self, action_id, request_options=None):
        """Retrieve a terminal action by ID."""
        return self._get(
            uri="/terminals/v1/actions/" + self._path_param(action_id),
            request_options=request_options,
        )

    def cancel_action(self, action_id, request_options=None):
        """Cancel a terminal action without a request body."""
        return self._post(
            uri="/terminals/v1/actions/" + self._path_param(action_id) + "/cancel",
            request_options=request_options,
        )

    def list(self, request_options=None):
        """List terminals registered to the authenticated account."""
        return self._get(uri="/terminals/v1/list", request_options=request_options)