"""Point-of-sale resource for managing POS locations."""
from mercadopago.core import MPBase


class POS(MPBase):
    """Manage points of sale linked to a Mercado Pago account."""

    def list_pos(self, user_id, request_options=None):
        """List points of sale for a user.

        Args:
            user_id: Identifier of the user whose POS devices are listed.
            request_options: Per-call configuration overrides.

        Returns:
            dict: The user's point-of-sale list.
        """
        return self._get(
            uri="/users/" + self._path_param(user_id) + "/pos",
            request_options=request_options,
        )

    def search_pos(self, filters=None, request_options=None):
        """Search for points of sale.

        Args:
            filters: Optional query filters: ``external_id``,
                ``external_store_id``, ``store_id``, and ``category``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Search results and paging information.
        """
        return self._get(
            uri="/pos",
            filters=filters,
            request_options=request_options,
        )

    def create_pos(self, pos_object, request_options=None):
        """Create a point of sale in a store.

        Args:
            pos_object: POSRequest JSON body as a dictionary.
            request_options: Per-call configuration overrides.

        Returns:
            dict: The created point of sale.
        """
        if not isinstance(pos_object, dict):
            raise ValueError("Param pos_object must be a Dictionary")

        return self._post(
            uri="/pos",
            data=pos_object,
            request_options=request_options,
        )

    def delete_pos(self, id, request_options=None):
        """Delete a point of sale.

        Args:
            id: Identifier of the point of sale to delete.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Deletion response.
        """
        return self._delete(
            uri="/pos/" + self._path_param(id),
            request_options=request_options,
        )

    def get_pos(self, id, request_options=None):
        """Get a point of sale by ID.

        Args:
            id: Identifier of the point of sale.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Point of sale details.
        """
        return self._get(
            uri="/pos/" + self._path_param(id),
            request_options=request_options,
        )

    def update_pos(self, id, pos_object, request_options=None):
        """Update a point of sale.

        Args:
            id: Identifier of the point of sale to update.
            pos_object: POSRequest JSON body as a dictionary.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Updated point of sale details.
        """
        if not isinstance(pos_object, dict):
            raise ValueError("Param pos_object must be a Dictionary")

        return self._put(
            uri="/pos/" + self._path_param(id),
            data=pos_object,
            request_options=request_options,
        )
