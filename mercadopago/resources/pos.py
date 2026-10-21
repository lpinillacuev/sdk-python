"""POS resource for searching and creating points of sale."""
from mercadopago.core import MPBase


class POS(MPBase):
    def delete_pos(self, pos_id, request_options=None):
        """Deletes a point of sale.

        Args:
            pos_id: Identifier of the point of sale to delete.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Deletion response and HTTP status.
        """
        return self._delete(uri="/pos/" + self._path_param(pos_id),
                            request_options=request_options)

    def list_pos(self, user_id, request_options=None):
        """Lists points of sale for a user.

        Args:
            user_id: Identifier of the user whose points of sale are listed.
            request_options: Per-call configuration overrides.

        Returns:
            dict: POS list and HTTP status.
        """
        return self._get(uri="/users/" + self._path_param(user_id) + "/pos",
                         request_options=request_options)

    def get_pos(self, pos_id, request_options=None):
        """Retrieves a point of sale by identifier.

        Args:
            pos_id: Identifier of the point of sale.
            request_options: Per-call configuration overrides.

        Returns:
            dict: POS details and HTTP status.
        """
        return self._get(uri="/pos/" + self._path_param(pos_id),
                         request_options=request_options)

    def update_pos(self, pos_id, pos_object, request_options=None):
        """Updates a point of sale.

        Args:
            pos_id: Identifier of the point of sale.
            pos_object: POSRequest dict containing ``name`` and ``store_id``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Updated POS details and HTTP status.

        Raises:
            ValueError: If *pos_object* is not a dict.
        """
        if not isinstance(pos_object, dict):
            raise ValueError("Param pos_object must be a Dictionary")
        return self._put(uri="/pos/" + self._path_param(pos_id),
                         data=pos_object, request_options=request_options)

    """Manages Mercado Pago points of sale."""

    def search_pos(self, filters=None, request_options=None):
        """Searches points of sale.

        Args:
            filters: Optional query parameters: ``external_id``,
                ``external_store_id``, ``store_id``, and ``category``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Paginated POS search results and HTTP status.
        """
        return self._get(uri="/pos", filters=filters, request_options=request_options)

    def create_pos(self, pos_object, request_options=None):
        """Creates a point of sale in a store.

        Args:
            pos_object: POSRequest dict with required ``name`` and ``store_id``;
                optional ``external_id``, ``external_store_id``, ``category``,
                ``fixed_amount``, and ``url``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Created POS and HTTP status.

        Raises:
            ValueError: If *pos_object* is not a dict.
        """
        if not isinstance(pos_object, dict):
            raise ValueError("Param pos_object must be a Dictionary")

        return self._post(uri="/pos", data=pos_object, request_options=request_options)