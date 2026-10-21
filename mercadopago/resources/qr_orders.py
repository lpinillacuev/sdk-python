"""QR Orders resource for confirming cash withdrawal orders."""
from mercadopago.core import MPBase


class QROrders(MPBase):
    """Manages QR-based in-store orders."""

    def confirm_cashout_qr(self, merchant_order_id, confirmation_object, request_options=None):
        """Confirms or cancels the cashout status of a QR withdrawal order.

        Args:
            merchant_order_id: Identifier of the merchant order.
            confirmation_object: Dict containing ``status`` (``confirmed`` or
                ``cancelled``).
            request_options: Per-call configuration overrides.

        Returns:
            dict: Cashout confirmation response.
        """
        if not isinstance(confirmation_object, dict):
            raise ValueError("Param confirmation_object must be a Dictionary")

        return self._post(
            uri=f"/instore/orders/{self._path_param(merchant_order_id)}/confirmation",
            data=confirmation_object,
            request_options=request_options,
        )