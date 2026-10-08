"""User, Store, and POS resources for the MercadoPago API.

The authenticated profile uses ``/users/me``. Store and POS methods map to
their own documented URIs and are not aliases for :meth:`User.get`.
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
        return self._post(
            uri=f"/users/{self._path_param(user_id)}/stores",
            data=store_object,
            request_options=request_options,
        )

    def search_stores(self, user_id, filters=None, request_options=None):
        """Searches stores belonging to a user."""
        return self._get(
            uri=f"/users/{self._path_param(user_id)}/stores/search",
            filters=filters,
            request_options=request_options,
        )

    def get_store(self, store_id, request_options=None):
        """Retrieves a store by ID."""
        return self._get(
            uri=f"/stores/{self._path_param(store_id)}",
            request_options=request_options,
        )

    def update_store(self, user_id, store_id, store_object, request_options=None):
        """Updates a store belonging to a user."""
        return self._put(
            uri=(f"/users/{self._path_param(user_id)}/stores/"
                 f"{self._path_param(store_id)}"),
            data=store_object,
            request_options=request_options,
        )

    def delete_store(self, user_id, store_id, request_options=None):
        """Deletes a store belonging to a user."""
        return self._delete(
            uri=(f"/users/{self._path_param(user_id)}/stores/"
                 f"{self._path_param(store_id)}"),
            request_options=request_options,
        )

    def search_pos(self, filters=None, request_options=None):
        """Searches points of sale."""
        return self._get(uri="/pos", filters=filters,
                         request_options=request_options)

    def create_pos(self, pos_object, request_options=None):
        """Creates a point of sale."""
        return self._post(uri="/pos", data=pos_object,
                          request_options=request_options)

    def get_pos(self, pos_id, request_options=None):
        """Retrieves a point of sale by ID."""
        return self._get(uri=f"/pos/{self._path_param(pos_id)}",
                         request_options=request_options)

    def update_pos(self, pos_id, pos_object, request_options=None):
        """Updates a point of sale."""
        return self._put(uri=f"/pos/{self._path_param(pos_id)}",
                         data=pos_object, request_options=request_options)

    def delete_pos(self, pos_id, request_options=None):
        """Deletes a point of sale."""
        return self._delete(uri=f"/pos/{self._path_param(pos_id)}",
                            request_options=request_options)

    def list_pos(self, user_id, request_options=None):
        """Lists points of sale belonging to a user."""
        return self._get(uri=f"/users/{self._path_param(user_id)}/pos",
                         request_options=request_options)

    @property
    def request_options(self):
        """Default :class:`RequestOptions` for this resource instance."""
        return self.__request_options
