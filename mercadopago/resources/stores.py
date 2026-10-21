"""Stores resource for the MercadoPago API."""
from mercadopago.core import MPBase


class Stores(MPBase):
    """Retrieves stores belonging to the authenticated account."""

    def create_store(self, user_id, store_object, request_options=None):
        """Creates a store for a user.

        Args:
            user_id: Identifier of the store owner.
            store_object: Store data including the required ``name``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Created store and HTTP status.
        """
        if not isinstance(store_object, dict):
            raise ValueError("Param store_object must be a Dictionary")

        return self._post(
            uri="/users/" + self._path_param(user_id) + "/stores",
            data=store_object,
            request_options=request_options,
        )

    def search_stores(self, user_id, filters=None, request_options=None):
        """Searches a user's stores.

        Args:
            user_id: Identifier of the store owner.
            filters: Query parameters, such as ``external_id``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Matching stores and HTTP status.
        """
        return self._get(
            uri="/users/" + self._path_param(user_id) + "/stores/search",
            filters=filters,
            request_options=request_options,
        )

    def delete_store(self, user_id, id, request_options=None):  # pylint: disable=redefined-builtin
        """Deletes a user's store.

        Args:
            user_id: Identifier of the store owner.
            id: Store identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Deletion response and HTTP status.
        """
        return self._delete(
            uri="/users/" + self._path_param(user_id) + "/stores/" + self._path_param(id),
            request_options=request_options,
        )

    def update_store(self, user_id, id, store_object, request_options=None):  # pylint: disable=redefined-builtin
        """Updates a user's store.

        Args:
            user_id: Identifier of the store owner.
            id: Store identifier.
            store_object: StoreRequest data including the required ``name``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Updated store and HTTP status.
        """
        if not isinstance(store_object, dict):
            raise ValueError("Param store_object must be a Dictionary")

        return self._put(
            uri="/users/" + self._path_param(user_id) + "/stores/" + self._path_param(id),
            data=store_object,
            request_options=request_options,
        )

    def get_store(self, id, request_options=None):  # pylint: disable=redefined-builtin
        """Retrieves a store by its ID.

        Args:
            id: Store identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Store details and HTTP status.
        """
        return self._get(
            uri="/stores/" + self._path_param(id),
            request_options=request_options,
        )