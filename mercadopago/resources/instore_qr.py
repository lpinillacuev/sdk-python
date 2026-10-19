"""In-store QR order endpoints."""

from mercadopago.core import MPBase


class InstoreQR(MPBase):
    """Manage QR-based in-store orders."""

    def create_qr_tramma_dynamic(self, user_id, external_pos_id, order_object,
                                 request_options=None):
        """Create a dynamic QR trama for a seller's point of sale."""
        if not isinstance(order_object, dict):
            raise ValueError("Param order_object must be a Dictionary")
        return self._post(
            uri=f"/instore/orders/qr/seller/collectors/{self._path_param(user_id)}"
            f"/pos/{self._path_param(external_pos_id)}/qrs",
            data=order_object,
            request_options=request_options,
        )

    def create_dynamic_qr_order(self, user_id, external_pos_id, order_object,
                                request_options=None):
        """Create a dynamic QR order at a seller's point of sale."""
        if not isinstance(order_object, dict):
            raise ValueError("Param order_object must be a Dictionary")
        return self._put(
            uri=f"/instore/orders/qr/seller/collectors/{self._path_param(user_id)}"
            f"/pos/{self._path_param(external_pos_id)}/qrs",
            data=order_object,
            request_options=request_options,
        )

    def confirm_cashout_qr(self, merchant_order_id, confirmation_object,
                           request_options=None):
        """Confirm or cancel a QR cashout order with a status payload."""
        if not isinstance(confirmation_object, dict):
            raise ValueError("Param confirmation_object must be a Dictionary")
        return self._post(
            uri=f"/instore/orders/{self._path_param(merchant_order_id)}/confirmation",
            data=confirmation_object,
            request_options=request_options,
        )

    def delete_instore_order_v2(self, user_id, external_pos_id, request_options=None):
        """Delete a V2 QR order at a seller's point of sale."""
        return self._delete(
            uri=f"/instore/qr/seller/collectors/{self._path_param(user_id)}"
            f"/pos/{self._path_param(external_pos_id)}/orders",
            request_options=request_options,
        )

    def get_instore_order_v2(self, user_id, external_pos_id, request_options=None):
        """Retrieve a V2 QR order at a seller's point of sale."""
        return self._get(
            uri=f"/instore/qr/seller/collectors/{self._path_param(user_id)}"
            f"/pos/{self._path_param(external_pos_id)}/orders",
            request_options=request_options,
        )

    def create_instore_order_v2(self, user_id, external_store_id, external_pos_id,
                                order_object, request_options=None):
        """Create a V2 QR order for a store and point of sale."""
        if not isinstance(order_object, dict):
            raise ValueError("Param order_object must be a Dictionary")
        return self._put(
            uri=f"/instore/qr/seller/collectors/{self._path_param(user_id)}"
            f"/stores/{self._path_param(external_store_id)}"
            f"/pos/{self._path_param(external_pos_id)}/orders",
            data=order_object,
            request_options=request_options,
        )

    def delete_instore_order_v1(self, user_id, external_id, request_options=None):
        """Delete a V1 in-store QR order."""
        return self._delete(
            uri=f"/mpmobile/instore/qr/{self._path_param(user_id)}"
            f"/{self._path_param(external_id)}",
            request_options=request_options,
        )

    def create_instore_order_v1(self, user_id, external_id, order_object,
                                request_options=None):
        """Create a V1 in-store QR order."""
        if not isinstance(order_object, dict):
            raise ValueError("Param order_object must be a Dictionary")
        return self._put(
            uri=f"/mpmobile/instore/qr/{self._path_param(user_id)}"
            f"/{self._path_param(external_id)}",
            data=order_object,
            request_options=request_options,
        )