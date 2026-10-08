"""User-scoped Stores, POS, and QR API operations."""
import warnings

from mercadopago.core.mp_base import MPBase


class User(MPBase):  # pylint: disable=too-many-public-methods
    """Exposes Stores, POS, QR Integrator, and QR order operations."""

    def get(self, request_options=None):
        """Retrieves the authenticated user."""
        return self._get("/users/me", request_options=request_options)

    def create_store(self, user_id, store_object, request_options=None):
        """Creates a store for a user."""
        return self._post(
            f"/users/{self._path_param(user_id)}/stores",
            store_object,
            request_options=request_options,
        )

    def get_store(self, store_id, request_options=None):
        """Retrieves a store by ID."""
        return self._get(
            f"/stores/{self._path_param(store_id)}",
            request_options=request_options,
        )

    def search_stores(self, user_id, filters=None, request_options=None):
        """Searches stores owned by a user."""
        return self._get(
            f"/users/{self._path_param(user_id)}/stores/search",
            filters,
            request_options,
        )

    def update_store(self, user_id, store_id, store_object, request_options=None):
        """Updates a store."""
        return self._put(
            f"/users/{self._path_param(user_id)}/stores/"
            f"{self._path_param(store_id)}",
            store_object,
            request_options=request_options,
        )

    def delete_store(self, user_id, store_id, request_options=None):
        """Deletes a store."""
        return self._delete(
            f"/users/{self._path_param(user_id)}/stores/"
            f"{self._path_param(store_id)}",
            request_options=request_options,
        )

    def search_pos(self, filters=None, request_options=None):
        """Searches points of sale."""
        return self._get("/pos", filters, request_options)

    def create_pos(self, pos_object, request_options=None):
        """Creates a point of sale."""
        return self._post("/pos", pos_object, request_options=request_options)

    def get_pos(self, pos_id, request_options=None):
        """Retrieves a point of sale."""
        return self._get(
            f"/pos/{self._path_param(pos_id)}",
            request_options=request_options,
        )

    def update_pos(self, pos_id, pos_object, request_options=None):
        """Updates a point of sale."""
        return self._put(
            f"/pos/{self._path_param(pos_id)}",
            pos_object,
            request_options=request_options,
        )

    def delete_pos(self, pos_id, request_options=None):
        """Deletes a point of sale."""
        return self._delete(
            f"/pos/{self._path_param(pos_id)}",
            request_options=request_options,
        )

    def list_pos(self, user_id, request_options=None):
        """Lists points of sale for a user."""
        return self._get(
            f"/users/{self._path_param(user_id)}/pos",
            request_options=request_options,
        )

    def configure_qr_integrator(self, config_object, request_options=None):
        """Creates or updates QR integrator configuration.

        The API operation uses PATCH. This SDK's shared transport currently
        exposes only GET, POST, PUT, and DELETE helpers, so the operation is
        intentionally rejected rather than sent with the wrong HTTP method.
        """
        del config_object, request_options
        raise NotImplementedError(
            "PATCH /instore/integrator is not supported by this SDK transport"
        )

    def get_qr_integrator(self, request_options=None):
        """Retrieves QR integrator configuration."""
        return self._get("/instore/integrator", request_options=request_options)

    def confirm_cashout_qr(
        self, merchant_order_id, confirmation_object, request_options=None
    ):
        """Confirms QR cashout status."""
        return self._post(
            f"/instore/orders/{self._path_param(merchant_order_id)}/confirmation",
            confirmation_object,
            request_options=request_options,
        )

    def get_instore_order_v2(self, user_id, external_pos_id, request_options=None):
        """Retrieves a deprecated V2 in-store order."""
        return self._get(
            f"/instore/qr/seller/collectors/{self._path_param(user_id)}/pos/"
            f"{self._path_param(external_pos_id)}/orders",
            request_options=request_options,
        )

    def delete_instore_order_v2(self, user_id, external_pos_id, request_options=None):
        """Deletes a deprecated V2 in-store order."""
        return self._delete(
            f"/instore/qr/seller/collectors/{self._path_param(user_id)}/pos/"
            f"{self._path_param(external_pos_id)}/orders",
            request_options=request_options,
        )

    def create_instore_order_v1(
        self, user_id, external_id, order_object, request_options=None
    ):
        """Creates a deprecated V1 in-store order."""
        return self._put(
            f"/mpmobile/instore/qr/{self._path_param(user_id)}/"
            f"{self._path_param(external_id)}",
            order_object,
            request_options=request_options,
        )

    def delete_instore_order_v1(self, user_id, external_id, request_options=None):
        """Deletes a deprecated V1 in-store order."""
        return self._delete(
            f"/mpmobile/instore/qr/{self._path_param(user_id)}/"
            f"{self._path_param(external_id)}",
            request_options=request_options,
        )

    def create_instore_order_v2(
        self,
        user_id,
        external_store_id,
        external_pos_id,
        order_object,
        request_options=None,
    ):
        """Creates a deprecated V2 in-store order."""
        return self._put(
            f"/instore/qr/seller/collectors/{self._path_param(user_id)}/stores/"
            f"{self._path_param(external_store_id)}/pos/"
            f"{self._path_param(external_pos_id)}/orders",
            order_object,
            request_options=request_options,
        )

    def create_qr_tramma_dynamic(
        self, user_id, external_pos_id, order_object, request_options=None
    ):
        """Creates a deprecated dynamic QR trama."""
        return self._post(
            f"/instore/orders/qr/seller/collectors/{self._path_param(user_id)}/pos/"
            f"{self._path_param(external_pos_id)}/qrs",
            order_object,
            request_options=request_options,
        )

    def create_dynamic_qr_order(
        self, user_id, external_pos_id, order_object, request_options=None
    ):
        """Creates a deprecated dynamic QR order."""
        return self._put(
            f"/instore/orders/qr/seller/collectors/{self._path_param(user_id)}/pos/"
            f"{self._path_param(external_pos_id)}/qrs",
            order_object,
            request_options=request_options,
        )