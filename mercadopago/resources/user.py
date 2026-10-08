"""User, Store, and POS resources for the MercadoPago API.

Wraps the authenticated user profile and the Store and POS operations
that historically belong to the SDK's User resource.
"""
from mercadopago.core import MPBase


class User(MPBase):
    """Retrieves the authenticated user's account information.

    Returns details such as user ID, email, site (country), and account
    status for the access token in use.
    """

    def get(self, request_options=None):
        """Retrieves the authenticated user's profile."""
        return self._get(uri="/users/me", request_options=request_options)

    def create_store(self, user_id, store_object, request_options=None):
        """Creates a store for a user."""
        if not isinstance(store_object, dict):
            raise ValueError("Param store_object must be a Dictionary")
        return self._post(
            uri="/users/" + self._path_param(user_id) + "/stores",
            data=store_object,
            request_options=request_options,
        )

    def get_store(self, store_id, request_options=None):
        """Retrieves a store by ID."""
        return self._get(
            uri="/stores/" + self._path_param(store_id),
            request_options=request_options,
        )

    def search_stores(self, user_id, filters=None, request_options=None):
        """Searches a user's stores, optionally by ``external_id``."""
        return self._get(
            uri="/users/" + self._path_param(user_id) + "/stores/search",
            filters=filters,
            request_options=request_options,
        )

    def update_store(self, user_id, store_id, store_object, request_options=None):
        """Updates a store."""
        if not isinstance(store_object, dict):
            raise ValueError("Param store_object must be a Dictionary")
        return self._put(
            uri=("/users/" + self._path_param(user_id) + "/stores/"
                 + self._path_param(store_id)),
            data=store_object,
            request_options=request_options,
        )

    def delete_store(self, user_id, store_id, request_options=None):
        """Deletes a store."""
        return self._delete(
            uri=("/users/" + self._path_param(user_id) + "/stores/"
                 + self._path_param(store_id)),
            request_options=request_options,
        )

    def create_pos(self, pos_object, request_options=None):
        """Creates a point of sale using a POSRequest-compatible dictionary."""
        if not isinstance(pos_object, dict):
            raise ValueError("Param pos_object must be a Dictionary")
        return self._post(uri="/pos", data=pos_object,
                          request_options=request_options)

    def get_pos(self, pos_id, request_options=None):
        """Retrieves a point of sale by ID."""
        return self._get(uri="/pos/" + self._path_param(pos_id),
                         request_options=request_options)

    def search_pos(self, filters=None, request_options=None):
        """Searches points of sale using the API's POS query filters."""
        return self._get(uri="/pos", filters=filters,
                         request_options=request_options)

    def update_pos(self, pos_id, pos_object, request_options=None):
        """Updates a point of sale."""
        if not isinstance(pos_object, dict):
            raise ValueError("Param pos_object must be a Dictionary")
        return self._put(uri="/pos/" + self._path_param(pos_id),
                         data=pos_object, request_options=request_options)

    def delete_pos(self, pos_id, request_options=None):
        """Deletes a point of sale."""
        return self._delete(uri="/pos/" + self._path_param(pos_id),
                            request_options=request_options)

    def list_pos(self, user_id, request_options=None):
        """Lists points of sale for a user."""
        return self._get(
            uri="/users/" + self._path_param(user_id) + "/pos",
            request_options=request_options,
        )


# Stores and POS share the historical User resource implementation.  These
# aliases provide tag-oriented SDK factories without duplicating HTTP logic.
Store = User
POS = User
