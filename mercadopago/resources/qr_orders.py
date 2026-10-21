"""QR Orders resource for confirming in-store cashout orders."""
from mercadopago.core import MPBase


class QROrders(MPBase):
    """Manages QR-based cashout order confirmations."""

    def confirm_cashout_qr(self, merchant_order_id, confirmation_object, request_options=None):
        """Confirms or cancels a QR cashout order.

        Args:
            merchant_order_id: Identifier of the merchant order to confirm.
            confirmation_object: Dict with ``status`` (``confirmed`` or ``cancelled``).
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *confirmation_object* is not a ``dict``.

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