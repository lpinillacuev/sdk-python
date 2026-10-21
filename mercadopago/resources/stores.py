"""Stores resource for the MercadoPago API."""
from mercadopago.core import MPBase


class Stores(MPBase):
    """Retrieves stores belonging to the authenticated account."""

    def get_store(self, id, request_options=None):
        """Retrieves a store by its ID.

        Args:
            id: Store ID.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Store details and HTTP status.
        """
        return self._get(
            uri="/stores/" + self._path_param(id),
            request_options=request_options,
        )

    def create_store(self, user_id, store_object, request_options=None):
        """Creates a store for a user.

        Args:
            user_id: Identifier of the store owner.
            store_object: Store data dict, including the required name.
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

    def search_stores(self, user_id, external_id=None, request_options=None):
        """Searches a user's stores by optional external ID.

        Args:
            user_id: Identifier of the store owner.
            external_id: Optional external store ID query filter.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Store search results and HTTP status.
        """
        filters = {"external_id": external_id} if external_id is not None else None
        return self._get(
            uri="/users/" + self._path_param(user_id) + "/stores/search",
            filters=filters,
            request_options=request_options,
        )

    def delete_store(self, user_id, id, request_options=None):
        """Deletes a store belonging to a user.

        Args:
            user_id: Identifier of the store owner.
            id: Store ID.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Deletion response and HTTP status.
        """
        return self._delete(
            uri="/users/" + self._path_param(user_id) + "/stores/" + self._path_param(id),
            request_options=request_options,
        )

    def update_store(self, user_id, id, store_object, request_options=None):
        """Updates a store belonging to a user.

        Args:
            user_id: Identifier of the store owner.
            id: Store ID.
            store_object: StoreRequest data dict, including the required name.
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