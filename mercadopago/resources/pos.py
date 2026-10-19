"""Point of sale resource for the Mercado Pago API."""
from mercadopago.core import MPBase


class POS(MPBase):
    """Searches and creates points of sale for the authenticated seller."""

    def list_pos(self, user_id, request_options=None):
        """List points of sale belonging to a user."""
        return self._get(
            uri="/users/" + self._path_param(user_id) + "/pos",
            request_options=request_options,
        )

    def search_pos(self, filters=None, request_options=None):
        """Search points of sale using optional external and store identifiers or category.

        Args:
            filters: Query parameters such as external_id, external_store_id,
                store_id, and category.
            request_options: Per-call configuration overrides.

        Returns:
            dict: API response containing paging and results.
        """
        return self._get(uri="/pos", filters=filters, request_options=request_options)

    def create_pos(self, data, request_options=None):
        """Create a point of sale in a store.

        Args:
            data: POS request body with name and store_id, and optional
                external_id, external_store_id, category, fixed_amount, or url.
            request_options: Per-call configuration overrides.

        Returns:
            dict: API response containing the created POS.
        """
        return self._post(uri="/pos", data=data, request_options=request_options)

    def delete_pos(self, pos_id, request_options=None):
        """Delete a point of sale by its identifier (DELETE /pos/{id})."""
        return self._delete(
            uri="/pos/" + self._path_param(pos_id),
            request_options=request_options,
        )

    def get_pos(self, pos_id, request_options=None):
        """Retrieve a point of sale by its identifier (GET /pos/{id})."""
        return self._get(
            uri="/pos/" + self._path_param(pos_id),
            request_options=request_options,
        )

    def update_pos(self, pos_id, data, request_options=None):
        """Update a point of sale with a POSRequest JSON body (PUT /pos/{id})."""
        return self._put(
            uri="/pos/" + self._path_param(pos_id),
            data=data,
            request_options=request_options,
        )