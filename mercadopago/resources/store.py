"""Store resource for the MercadoPago Stores API."""
from mercadopago.core import MPBase


class Store(MPBase):
    """Retrieves stores associated with a seller account."""

    def get(self, store_id, request_options=None):
        """Retrieves a store by its ID.

        Args:
            store_id: Unique identifier of the store.
            request_options: Per-call configuration overrides.

        Returns:
            dict: API response containing the store JSON.
        """
        return self._get(
            uri="/stores/" + self._path_param(store_id),
            request_options=request_options,
        )

    def create_store(self, user_id, store_object, request_options=None):
        """Creates a store for a user from a StoreRequest JSON object."""
        if not isinstance(store_object, dict):
            raise ValueError("Param store_object must be a Dictionary")
        if not isinstance(store_object.get("name"), str):
            raise ValueError("Param store_object must contain a name")

        return self._post(
            uri="/users/" + self._path_param(user_id) + "/stores",
            data=store_object,
            request_options=request_options,
        )

    def search_stores(self, user_id, external_id=None, request_options=None):
        """Searches a user's stores, optionally filtered by external_id."""
        filters = {"external_id": external_id} if external_id is not None else None
        return self._get(
            uri="/users/" + self._path_param(user_id) + "/stores/search",
            filters=filters,
            request_options=request_options,
        )

    def delete_store(self, user_id, store_id, request_options=None):
        """Deletes a store belonging to a user."""
        return self._delete(
            uri="/users/" + self._path_param(user_id) + "/stores/"
            + self._path_param(store_id),
            request_options=request_options,
        )

    def update_store(self, user_id, store_id, store_object, request_options=None):
        """Updates a store from a StoreRequest JSON object."""
        if not isinstance(store_object, dict):
            raise ValueError("Param store_object must be a Dictionary")
        if not isinstance(store_object.get("name"), str):
            raise ValueError("Param store_object must contain a name")

        return self._put(
            uri="/users/" + self._path_param(user_id) + "/stores/"
            + self._path_param(store_id),
            data=store_object,
            request_options=request_options,
        )